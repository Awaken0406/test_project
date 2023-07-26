const http = require('http');
const mysql = require('mysql');
const url = require('url');
const fs = require('fs');

const con = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '123456',
  database: 'senge'
});

con.connect(function(err) {
    if (err) {
      console.error('Error connecting to MySQL database: ' + err.stack);
      return;
    }
    console.log('Connected to MySQL database as id ' + con.threadId);
  });

/*这段代码创建了一个HTTP服务器，并使用MySQL模块连接到MySQL数据库。它还定义了三个路由：

“/”路由用于返回index.html页面。
“/gettable”路由用于返回数据库中所有表的名称。
“/getdata/:tablename”路由用于返回指定表中的所有记录。*/

const server = http.createServer(function(req, res) {
  const q = url.parse(req.url, true);
  const filename = '.' + q.pathname;

  if (filename === './') {
    fs.readFile('index.html', function(err, data) {
      if (err) {
        res.writeHead(404, {'Content-Type': 'text/html'});
        return res.end('404 Not Found');
      }
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.write(data);
      return res.end();
    });
  } else if (filename === './gettable') {
    con.query('SHOW TABLES', function(err, result) {
      if (err) throw err;
      res.writeHead(200, {'Content-Type': 'application/json'});
      res.write(JSON.stringify(result));
      console.log(result)
      return res.end();
    });
  } else if (q.pathname.startsWith('/getdata/')) {
    const tablename = decodeURIComponent(q.pathname.substring(9));
    con.query('SELECT * FROM ??', [tablename], function(err, result) {
      if (err) throw err;
      res.writeHead(200, {'Content-Type': 'application/json'});
      res.write(JSON.stringify(result));
      return res.end();
    });
  } else {
    fs.readFile(filename, function(err, data) {
      if (err) {
        res.writeHead(404, {'Content-Type': 'text/html'});
        return res.end('404 Not Found');
      }
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.write(data);
      return res.end();
    });
  }
});

server.listen(8080, function() {
  console.log('Server listening on port 8080');
});
//npm install mysql
