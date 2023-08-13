import asyncio
import logging
import os

import grpc
from tracker_pb2_grpc import *
from tracker_pb2 import *
import pymongo
from pymongo import MongoClient
import aio_pika

mongo_endpt = os.environ.get('MONGO_DB_ENDPT')
queue_endpt = os.environ.get('RABBITMQ_URL')

class Tracker(TrackerServicer):

    CONNECTION_PORT = 5672
    CREDS = aio_pika.credentials.PlainCredentials('admin','admin')

    def __init__(self):
        if not mongo_endpt:
            raise Exception('Mongo endpoint is missing!')

        self.mongo_client = MongoClient(str(mongo_endpt) + ':27017')

    async def GetVehicles(
        self, request: GetVehiclesRequest, context: grpc.aio.ServicerContext
    ) -> GetVehiclesResponse:
        logging.info("Sending list of vehicles to be tracked.")
        return await GetVehiclesResponse(vehicle_names=await self.fetchVehicleNamesFromDatabase())

    async def fetchVehicleNamesFromDatabase():
        logging.info('Fetching delivery vehicles from the database.')
        mydb = mongo_client["Delivery"]
        return await mydb.list_collection_names()

    async def create_channel(self):
        return await aio_pika.connect_robust("amqp://" + queue_endpt + ':5672', loop=asyncio.get_event_loop())

    async def StreamVehicleCoordinates(
        self, request: StreamVehicleCoordinatesRequest, context: grpc.aio.ServicerContext
    ) -> StreamVehicleCoordinatesResponse:
        logging.info('Streaming vehicle coordinates from message queue ' + str(request.vehicle_name))
        queuename = request.vehicle_name

        async with self.create_channel() as channel:
            queue = await channel.declare_queue(queuename)
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        body = message.body.decode()
                        logger.debug('Received a message: ' + body)
                        msg = eval(body)
                        vehicle_record = VehicleRecord(
                            truck_type=msg['truck_type'],
                            truck_number=msg['truck_number'],
                            timestamp=msg['timestamp'],
                            coordinates=msg['coordinates']
                        )
                        yield StreamVehicleCoordinatesResponse(vehicleRecord=vehicle_record)

async def serve() -> None:
    server = grpc.aio.server()
    add_TrackerServicer_to_server(Tracker(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    LOG_FORMAT = '%(asctime)s - %(lineno)s:%(funcName)s - %(levelname)s - %(message)s'
    # LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                #   '-35s %(lineno) -5d: %(message)s')
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    asyncio.run(serve()) 
