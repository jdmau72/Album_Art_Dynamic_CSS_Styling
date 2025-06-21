// const { exec } = require('child_process');
//
// exec ('python3.12 ThemeExtractor.py', (error, stdout, stderr) => {
//
//     console.log(stdout);
//
// });
console.log("Hello World");

const spawn = require('node:child_process').spawn;
const pythonProcess = spawn('python3', ['ThemeExtractor.py'], {detached:true,});

pythonProcess.stdout.on('data', data => {
    console.log(data.toString());
});


