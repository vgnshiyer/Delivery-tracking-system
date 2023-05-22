FROM node:lts

WORKDIR app

ADD . /app/

# building the app
RUN npm install
RUN npm install mapbox-gl --save
RUN npm run build

# Expose port 3000
EXPOSE 3000

# Running the app
CMD [ "npm", "run", "dev" ]