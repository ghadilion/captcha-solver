function toDataURL(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
      var reader = new FileReader();
      reader.onloadend = function() {
        callback(reader.result);
      }
      reader.readAsDataURL(xhr.response);
    };
    xhr.open('GET', url);
    xhr.responseType = 'blob';
    xhr.send();
  }
  
var xhr1 = new XMLHttpRequest();
var url1 = "http://127.0.0.1:5001/solvecaptcha";
xhr1.open("POST", url1, true);
xhr1.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
xhr1.onreadystatechange = function () {
    if (xhr1.readyState === 4 && xhr1.status === 200) {
      var json = JSON.parse(xhr1.responseText);
      var inputField = document.getElementById('captchacharacters');
      inputField.value = json.captcha_text;
      inputField.style.backgroundColor = '#5ced73';
    }
};

window.addEventListener('load', function () {
  toDataURL(document.getElementsByTagName('img')[0].src, function(dataUrl) {
    console.log(dataUrl)  
    xhr1.send(JSON.stringify({"image": dataUrl}));
  })
})


