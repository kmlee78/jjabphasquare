const loading = document.querySelector("#loading");
const submit_btn = document.querySelector("#submit-btn");
const result = document.querySelector("#result");

submit_btn.addEventListener("click", function(e){
    loading.classList.remove("not-visible");
})

if (result == null) {
    loading.classList.add("not-visible");
}