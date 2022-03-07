// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

export default function handler(req, res) {
  var jsonvar = {"names":"abcd"}
  res.status(200).json(jsonvar)
}
