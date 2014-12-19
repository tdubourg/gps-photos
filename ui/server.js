"use strict"

var http = require("http"),
    url = require("url"),
    fs = require("fs"),
    path = require("path"),
    port = process.argv[2] || 80;

http.createServer(function(request, response) {

  var uri = url.parse(request.url).pathname
    , filename = path.join(process.cwd(), uri);
  


  fs.exists(filename, function(exists) {
    if(!exists || fs.statSync(filename).isDirectory()) {
      response.writeHead(404, {"Content-Type": "text/plain"});
      response.write("404 Not Found\n");
      response.end();
      return;
    }
    
    // This line opens the file as a readable stream
    var readStream = fs.createReadStream(filename);
  
    // This will wait until we know the readable stream is actually valid before piping
    readStream.on('open', function () {
      // This just pipes the read stream to the response object (which goes to the client)
      readStream.pipe(response);
    });
  
    // This catches any errors that happen while creating the readable stream (usually invalid names)
    readStream.on('error', function(err) {
      response.end(err);
    });
//    fs.readFile(filename, "binary", function(err, file) {
//      if(err) {        
 //       response.writeHead(500, {"Content-Type": "text/plain"});
  //      response.write(err + "\n");
   //     response.end();
    //    return;
//      }
//
 //     response.writeHead(200);
  //    response.write(file, "binary");
   //   response.end();
    //});
  });
}).listen(parseInt(port, 10), "0.0.0.0");

console.log("Static file server running at\n  => http://0.0.0.0:" + port + "/\nCTRL + C to shutdown");


