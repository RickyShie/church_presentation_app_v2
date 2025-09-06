const socket = io();
const navLinks = document.querySelectorAll(".control_button");
navLinks.forEach( navLink => {
    navLink.addEventListener("click", () => {
        socket.emit("nav_clicked", {
          id: navLink.getAttribute("id"),
          text: navLink.textContent
        });
    })
});