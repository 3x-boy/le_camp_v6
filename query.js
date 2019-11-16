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
