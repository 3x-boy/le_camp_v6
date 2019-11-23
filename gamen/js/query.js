// 右クリック禁止
document.oncontextmenu = function () {return false;}

// 属性チェックボタンを押したら、選択した属性に表示する
$(function() { 
    $('input[name="kategory[]"]').change(function() {
        var kategorys = [];
   
      $('input[name="kategory[]"]:checked').each(function() {
        kategorys.push("　" + $(this).val());
      });
   
      $('#p01').text(kategorys);
    });
  });

// 属性クリア
$(function() {
  $('#clear').click(function() {
    $('input[name="kategory[]"]').prop('checked', false);
    $('#p01').text("");
    alert('OK');
  });
});

// サムネイルのチェックボックス
$(function() {
    // チェックボックスのクリックを無効化
    $('.image_box .disabled_checkbox').click(function() {
      return false;
    });
  
    // 画像がクリックされた時の処理
    $('img.thumbnail').on('click', function() {
      if (!$(this).is('.checked')) {
        $(this).addClass('checked');
      } else {
        $(this).removeClass('checked')
      }
    });
});

// 読込中
/* ------------------------------
 Loading イメージ表示関数
 引数： msg 画面に表示する文言
 ------------------------------ */
function dispLoading(msg){
// 引数なし（メッセージなし）を許容
if( msg == undefined ){
    msg = "";
}
// 画面表示メッセージ
var dispMsg = "<div class='loadingMsg'>" + msg + "</div>";
// ローディング画像が表示されていない場合のみ出力
if($("#loading").length == 0){
    $("body").append("<div id='loading'>" + dispMsg + "</div>");
    }
}

/* ------------------------------
Loading イメージ削除関数
------------------------------ */
function removeLoading(){
    $("#loading").remove();
}

/* ------------------------------
 非同期処理の組み込みイメージ
 ------------------------------ */
 $(function () {
    $("#submit").click( function() {
   
      // 処理前に Loading 画像を表示
      dispLoading("処理中...");
   
      // 非同期処理
      $.ajax({
        url: 'ajax_test.html',
        /* https://kinocolog.com/ajax/test.html というURL指定も可 */
        type: 'GET',
        dataType: 'html'
        //url : "http://localhost:8080/",
        //type:"POST",
        //dataType:"json"
        //data : {parameter1 : param1, parameter2 : param2 },
        //timeout:3000,
  })
      // 通信成功時
      .done( function(data) {
        showMsg("成功しました");
      })
      // 通信失敗時
      .fail( function(data) {
        showMsg("失敗しました");
      })
      // 処理終了時
      .always( function(data) {
        // Lading 画像を消す
        removeLoading();
      });
    });
  });

  // 動画ファイル選択
  $(function() {
     $('#files').css({
         'position': 'absolute',
         'top': '-9999px'
     }).change(function() {
         var val = $(this).val();
         var path = val.replace(/\\/g, '/');
         var match = path.lastIndexOf('/');
    $('#filename').css("display","inline-block");
         $('#filename').val(match !== -1 ? val.substring(match + 1) : val);
     });
     $('#filename').bind('keyup, keydown, keypress', function() {
         return false;
     });
     $('#filename, #btn').click(function() {
         $('#files').trigger('click');
     });
 });

 /* 画像1枚DL 
 $(function(){
  $(".download").on("click", function(e){
      $target = $(e.target);
      $target.attr({
          download: "img/welcome.jpg",
          href:  "img/welcome.jpg"
      });
  });
});

$(function() {
  $('.download').on('click', function(e){
    var href_url = $(this).attr('href');
    var href_name = $(this).attr('href').replace(/\\/g,'/').replace( /.*\//, '' );
    $(e.target).attr({
      download: "img/welcome.jpg",
      href: "img/welcome.jpg"
    });
  });
});*/

/** URLから画像DLリンクを作る関数 */
function downloadFromUrl(url, fileName){
  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  xhr.responseType = 'blob';
  xhr.onload = function(e){
    if(this.status == 200){
      var urlUtil = window.URL || window.webkitURL;
      var imgUrl = urlUtil.createObjectURL(this.response);
      var link = document.createElement('a');
      link.href=imgUrl;
      link.download = fileName;
      link.innerHTML = 'ここからダウンロードできるよ';
      document.body.appendChild(link);
    }
  alert('OK');
  };
  xhr.send();
}

$(function() {
  $('#save').click(function() {
    downloadFromUrl('img/welcome.jpg', 'img.png');
  });
});

/* エラーメッセージアラート */
$('#errMsg').click(function(){
  if(!confirm('ごめんなさい！解析不能です。。\n動画ファイルは、MVOかmp4を選択してください。')){
      /* キャンセルの時の処理 */
      return false;
  }else{
      /*　OKの時の処理 */
      location.href = '#';
  }
});

/* ボタン非活性 */
$('button').click(function() {
 
  $('input').prop('disabled', false);

})

/* チェックボックス（複数）の値 */
$('input:checked').each(function() {
 
  console.log($(this).val());

});
