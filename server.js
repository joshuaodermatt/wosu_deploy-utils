const express = require('express')
const bodyParser = require('body-parser')
const path = require('path');
const fs = require('fs')

const app = express()

app.use(bodyParser.json())
app.use(express.static('public'))


const port = 3000

let isConfigured = false

let persistence = null


function loadPersistenceData() {
  fs.readFile(__dirname + 'persisence.json', function(err, data) {
    if (err) throw err
    return JSON.parse(data)
  })
  throw Error('could not load persistence')
}

function init() {
  try {
    if (fs.existsSync(__dirname + '/persistence.json')) {
      isConfigured = true
      persistence = loadPersistenceData()
    }
  } catch(err) {
    console.error(err)
    app.exit(1)
  }

}

init()

app.post('/configure', (req, res) => {
  if (!isConfigured) {
    const body = req.body

    console.log(req)
    if (
        body.key.trim().length >= 12 &&
        body.folder.trim().length > 0
    ) {
      fs.writeFile(__dirname + '/persistence.json', JSON.stringify({key: body.key, folder: body.folder}), function (err) {
        if (err) throw err;
      });
      isConfigured = true
      res.send(200)
    } else {
      res.send(400)
    }
  } else {
    res.send(401)
  }
})

app.post('/', (req, res) => {
  console.log(__dirname)
  res.sendFile(path.join(__dirname + '/index.html'));
})

app.listen(port, () => {
  console.log(`listening on port: ${port}`)
})

