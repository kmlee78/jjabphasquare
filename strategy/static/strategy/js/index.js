const loading = document.querySelector("#loading");
const submit_btn = document.querySelector("#submit-btn");
const result = document.querySelector("#result");
const modal_btn = document.querySelector("#modal-btn");
const index_modal_btn = document.querySelector("#index-modal-btn");
const backtest_values = document.querySelectorAll(".backtest-input input");

submit_btn.addEventListener("click", function(e){
    loading.classList.remove("not-visible");
})

if (result == null) {
    loading.classList.add("not-visible");
}


function modal(id) {
    let zIndex = 9999;
    let modal = document.getElementById(id);
    let bg = document.createElement("div");
    bg.setStyle({
        position: "fixed",
        zIndex: zIndex,
        left: "0px",
        top: "0px",
        width: "100%",
        height: "100%",
        overflow: "auto",
        backgroundColor: "rgba(0,0,0,0.4)"
    });
    document.body.append(bg);
    modal.querySelector(".modal-close-btn").addEventListener("click", function() {
        bg.remove();
        modal.style.display = "none";
    });

    modal.setStyle({
        position: "fixed",
        display: "block",
        boxShadow: "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
        zIndex: zIndex + 1,
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        msTransform: "translate(-50%, -50%)",
        webkitTransform: "translate(-50%, -50%)"
    });
}

Element.prototype.setStyle = function(styles) {
    for (let k in styles) this.style[k] = styles[k];
    return this;
};

modal_btn.addEventListener("click", function() {
    modal("modal");
});
index_modal_btn.addEventListener("click", function() {
    modal("index-modal");
});
