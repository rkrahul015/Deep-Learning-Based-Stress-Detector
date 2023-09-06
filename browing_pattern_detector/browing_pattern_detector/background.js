
let access_token = "9876543wqasdfghjnbvcdrtuhjhy";

chrome.tabs.onActivated.addListener(function (activeInfo) {
    chrome.tabs.get(activeInfo.tabId,function (tab) {
        let y = tab.url;
        console.log("########################");
        console.log(y);
        console.log("########################");
        fetch('http://127.0.0.1:5000/send_url', {method : 'POST', body : JSON.stringify({url : y, access_key : access_token}), headers : {'Content-Type' : 'application/json'}}).then((data) => {
            console.log(data);
        }).catch((err) => {
            console.log(err);
        })
    });
})

chrome.tabs.onUpdated.addListener((tabId, change, tab) => {
    if (tab.active && change.url) {
        fetch('http://127.0.0.1:5000/send_url', {method : 'POST', body : JSON.stringify({url : change.url, access_key : access_token}), headers : {'Content-Type' : 'application/json'}}).then((data) => {
            console.log(data);
        }).catch((err) => {
            console.log(err);
        })
    }
});

var tabToUrl = {};
chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
    tabToUrl[tabId] = tab.url;
});

chrome.tabs.onRemoved.addListener(function (tabId, removeInfo) {
    console.log(tabToUrl[tabId]);
    var xhttp2 = new XMLHttpRequest();
    fetch('http://127.0.0.1:5000/send_url', {method : 'POST', body : JSON.stringify({url : change.url, access_key : access_token}), headers : {'Content-Type' : 'application/json'}}).then((data) => {
        console.log(data);
    }).catch((err) => {
        console.log(err);
    })
    xhttp2.send("url=" + tabToUrl[tabId]);
    delete tabToUrl[tabId];

});