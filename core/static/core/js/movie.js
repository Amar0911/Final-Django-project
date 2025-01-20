document.addEventListener("DOMContentLoaded", () => {
    const modals = document.querySelectorAll(".modal");
    modals.forEach((modal) => {
      modal.addEventListener("hidden.bs.modal", (event) => {
        const video = modal.querySelector("video");
        if (video) {
          video.pause(); 
          video.currentTime = 0; 
        }
      });
    });
  });