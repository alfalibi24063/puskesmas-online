
document.addEventListener("DOMContentLoaded", function () {
    // Efek muncul pada bagian Home
    const sections = document.querySelectorAll(
        ".hero-section, .info-section, .steps-section, .bottom-section"
    );

    sections.forEach(function (section, index) {
        section.style.opacity = "0";

        setTimeout(function () {
            section.style.transition = "opacity 0.6s ease";
            section.style.opacity = "1";
        }, index * 150);
    });

    // Konfirmasi sebelum pendaftaran
    document.querySelectorAll(".btn-daftar").forEach(function (button) {
        button.addEventListener("click", function (event) {
            const yakin = confirm(
                "Apakah Anda ingin melanjutkan ke pendaftaran konsultasi?"
            );

            if (!yakin) {
                event.preventDefault();
            }
        });
    });
});
