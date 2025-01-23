document.addEventListener("DOMContentLoaded", function () {
  const messages = document.getElementsByClassName("message-element");

  function fadeOut(el, speed) {
    let opacity = 1;
    const timer = setInterval(function () {
      if (opacity <= 0.1) {
        clearInterval(timer);
        el.style.display = "none";
        el.remove(); // Eliminar el elemento del DOM
      }
      el.style.opacity = opacity;
      opacity -= opacity * 0.1;
    }, speed);
  }

  setTimeout(function () {
    Array.from(messages).forEach(function (message, index) {
      setTimeout(function () {
        fadeOut(message, 50);
      }, index * 100);
    });
  }, 5000);

  const modals = document.querySelectorAll(".modal");
  const closeModals = document.querySelectorAll(".close");

  closeModals.forEach(function (closeModal) {
    closeModal.addEventListener("click", function () {
      modals.forEach(function (modal) {
        modal.style.display = "none";
      });
    });
  });

  window.addEventListener("click", function (event) {
    modals.forEach(function (modal) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    });
  });
});
