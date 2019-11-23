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
  });
});

// サムネイルのチェック
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
    msg = "Loading";
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
    $("#proc_button").click( function() {
   
      // 処理前に Loading 画像を表示
      dispLoading("処理中...");
   
      // 非同期処理
      $.ajax({
        url : "サーバーサイドの処理を行うURL",
        type:"GET",
        dataType:"json"
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