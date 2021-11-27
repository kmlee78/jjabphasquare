const form = document.querySelector("form");
const chart_box = document.querySelector(".chart-box");
const post_received = document.querySelector(".post-received");

function resizeIframe(obj) {
    obj.style.height = obj.contentWindow.document.documentElement.scrollHeight + 'px';
    obj.style.width = obj.contentWindow.document.documentElement.scrollWidth + 'px';
}

if (post_received != null && chart_box == null) {
        alert("차트를 찾을 수 없습니다. 종목 이름을 확인해주세요.");
}
