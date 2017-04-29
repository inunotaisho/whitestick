let puller = require('website-scraper');

var options = {
  urls: ['http://nodejs.org/'],
  directory: '/path/to/save/',
};
 
// with promise 
scrape(options).then((result) => {
    /* some code here */
// Downloading images, css files and scripts 
scrape({
  urls: ['http://nodejs.org/'],
  directory: '/path/to/save',
  sources: [
    {selector: 'img', attr: 'src'},
    //{selector: 'link[rel="stylesheet"]', attr: 'href'},
   // {selector: 'script', attr: 'src'}
  ]
}).then(console.log).catch(console.log);

}).catch((err) => {
    /* some code here */
});
 
// or with callback 
scrape(options, (error, result) => {
    /* some code here */
});