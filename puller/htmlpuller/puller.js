
let puller = require('website-scraper');
let options = {
urls: ['https://en.wikipedia.org/wiki/Baltimore/'],
directory: './textholder/mypage',
};

// with promise 
let promise = puller(options);

promise.then(function(result){
    console.log(result);
});

// promise.then((result) => {
//     /* some code here */
// // Downloading images, css files and scripts 
// 	puller({
// 	  urls: ['http://twitter.com/*'],
// 	  directory: '/path/to/save',
// 	  sources: [
// 	    {selector: 'img', attr: 'src'},
// 	    //{selector: 'link[rel="stylesheet"]', attr: 'href'},
// 	   // {selector: 'script', attr: 'src'}
// 	  ]
// 	}).then(console.log).catch(console.log);

// 	}).catch((err) => {
// 	    /*some code here */
// 	});
//  });
// or with callback 
puller(options, (error, result) => {
    /*some code here */
});

module.exports = puller;
