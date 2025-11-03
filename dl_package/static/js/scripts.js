// js/scripts.js

/**
 * ログアウトフォームを送信する処理を実行します。
 * この関数を呼び出すことで、POSTリクエストによりログアウト処理が開始されます。
 */
function submitLogoutForm() {
    const form = document.getElementById('logout-form');
    
    // フォームが存在するか確認
    if (form) {
        form.submit();
        console.log("ログアウトフォームを送信しました。");
    } else {
        console.error("ID 'logout-form' を持つフォームが見つかりません。");
    }
}

/**
 * ページが完全に読み込まれた後にイベントリスナーを設定します。
 */
document.addEventListener('DOMContentLoaded', function() {
    const logoutLink = document.getElementById('logout-link');
    
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            // リンクのデフォルト動作（ページ遷移など）をキャンセル
            e.preventDefault(); 
            
            // 定義した関数を呼び出してログアウト処理を実行
            submitLogoutForm();
        });
    }
});