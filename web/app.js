const providerModal = document.getElementById("providerModal");
const modelModal = document.getElementById("modelModal");

const openModalButton = document.getElementById("openModal");
const closeModalButton = document.getElementById("closeModal");
const cancelModalButton = document.getElementById("cancelModal");
const closeModelModalButton = document.getElementById("closeModelModal");

const testKeyButton = document.getElementById("testKey");

testKeyButton.addEventListener("click", () => {
  testKeyButton.textContent = "检测中...";
  setTimeout(() => {
    testKeyButton.textContent = "检测";
    alert("已发送测试请求（示意）");
  }, 800);
});

openModalButton.addEventListener("click", () => {
  modelModal.classList.add("open");
  modelModal.setAttribute("aria-hidden", "false");
});

[closeModalButton, cancelModalButton].forEach((button) => {
  button.addEventListener("click", () => {
    providerModal.classList.remove("open");
    providerModal.setAttribute("aria-hidden", "true");
  });
});

closeModelModalButton.addEventListener("click", () => {
  modelModal.classList.remove("open");
  modelModal.setAttribute("aria-hidden", "true");
});

window.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    providerModal.classList.remove("open");
    modelModal.classList.remove("open");
    providerModal.setAttribute("aria-hidden", "true");
    modelModal.setAttribute("aria-hidden", "true");
  }
});
