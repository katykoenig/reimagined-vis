const fs = require('fs');
const {exec} = require('child_process');

function executeCommandLineCmd(cmd) {
  return new Promise((resolve, reject) => {
    exec(cmd, (err, stdout, stderr) => {
      if (err) {
        reject(err);
      } else {
        resolve({stdout, stderr});
      }
    });
  });
}

const getFile = fileName => new Promise((resolve, reject) => {
  fs.readFile(fileName, 'utf8', (err, data) => {
    if (err) {
      console.log('READ FILE ERROR', fileName);
      reject(err);
      return;
    }
    resolve(data);
  });
});

const writeFile = (fileName, contents) => new Promise((resolve, reject) => {
  fs.writeFile(fileName, contents, (err) => {
    if (err) {
      console.log('WRITE FILE ERROR', fileName);
      reject(err);
      return;
    }
    resolve();
  });
});

const sleep = sleepTime => (...args) =>
  new Promise(resolve => setTimeout(() => resolve(...args), sleepTime));

function executePromisesInSeries(tasks) {
  return tasks.reduce((promiseChain, task) => promiseChain.then(task), Promise.resolve([]));
}

module.exports = {
  getFile: getFile,
  writeFile: writeFile,
  sleep: sleep,
  executeCommandLineCmd: executeCommandLineCmd,
  executePromisesInSeries: executePromisesInSeries
};
