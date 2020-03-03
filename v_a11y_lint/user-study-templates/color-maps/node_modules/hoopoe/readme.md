# Hoopoe
[![CircleCI](https://circleci.com/gh/mcnuttandrew/hoopoe.svg?style=svg)](https://circleci.com/gh/mcnuttandrew/hoopoe)

![hoopoe](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Common_Hoopoe_%28Upupa_epops%29_Photograph_by_Shantanu_Kuveskar.jpg/220px-Common_Hoopoe_%28Upupa_epops%29_Photograph_by_Shantanu_Kuveskar.jpg)

This library collects a number of server-side utility promises that I persistently find myself using across different projects. As the name of the library clearly indicates each of the commands in this library gives a promise. I don't guarantee that it will be in anyway useful to you or better than a similar promise library, but I still hope you like it.

Requirements: node with access to fs and child_process. I believe this means node v>6, but I am not 100% sure. It will not work in the browser.

Installation: npm install hoopoe

### executeCommandLineCmd(cmd)

Executes a string of command, and returns an object of as argument to next promise {stdout, stderr}.

### getFile(fileName)

Get a target file, returns a promise containing the file.

### writeFile(fileName, contents)

Write file contents to target file name, returns a promise that finishes after the file is written.

### sleep (sleeptime)

Higher order promise, returns a promise generating function. Can be used to sleep a promise, useful for lots of things. Features pass argument pass through, so if Example usage

```js
Promise.resolve()
  .then(() => [1, 2, 3])
  .then(sleep(30))
  .then(x => console.log(x)) // [1, 2, 3]
```

### executePromisesInSeries([() => Promise])

Execute an array of promises in series. Equivalent to the non-existent Promise.each. The main gotcha with this function is not accidentally triggered the promises early.
