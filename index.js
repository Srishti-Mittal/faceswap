const express = require('express')
const { spawn } = require('child_process')
const app = express()
const path=require("path");
const ejs=require("ejs");
const multer = require('multer')
// hello
const upload = multer({
  dest: 'data',
  limits: {
    fileSize: 1000000,
  },
  
  fileFilter(req, file, cb) {
  
  if (!file.originalname.match(/\.(png|jpg|jpeg)$/)){
    cb(new Error('Please upload an image.'))
  }
    cb(undefined, true)
  }
})
  
app.set('view engine', 'ejs');

app.use(express.static(path.resolve(__dirname,'public')));

app.post('/upload', upload.array('upload'), (req, res) => {
  if(req.files.length){
    if(req.files.length !== 2){
      console.log("in error")
      return res.render('pages/index',{error: "Please upload 2 images"});
    }
    console.log("Number of Files",req.files.length)
    const python = spawn('python', ['main.py',`data/`+req.files[0].filename,`data/`+req.files[1].filename])
    var output="";
    python.stdout.on('data', function (data) {
      console.log('Pipe data from python script ...')
      console.log(data.toString())
      output+= data
    })
    
      python.on('close', function (code) {
        // console.log("Output ",output.toString(),"end")
        console.log("Code is",code)
        res.render('pages/image',{image1: "img1.jpeg",image2: "img2.jpeg"});

      })
    
    
  }else{
    res.status(400).json({msg:"Img Not Received"})
  }
})

app.get('/upload',(req,res)=>{
  console.log("Check Route")
  res.render('pages/image',{image1: "img1.jpeg",image2: "img2.jpeg"});
})

app.get('/',(req,res)=>{
  console.log("Home Route")
  res.render('pages/index');
})

const PORT = process.env.PORT || 5000;


app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}!`)
})
