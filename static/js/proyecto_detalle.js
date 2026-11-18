document.addEventListener('DOMContentLoaded', () => {
    const visor = document.querySelector('.visor');
    if (!visor || typeof visor.showModal !== 'function') {
        return;
    }
    const imagen = visor.querySelector('.visor__imagen');
    const cerrar = visor.querySelector('.visor__cerrar');
    let origen = null;

    document.querySelectorAll('[data-ampliar]').forEach((enlace) => {
        enlace.addEventListener('click', (evento) => {
            evento.preventDefault();
            origen = enlace;
            imagen.src = enlace.href;
            imagen.alt = enlace.dataset.alt || '';
            visor.showModal();
            cerrar.focus();
        });
    });

    cerrar.addEventListener('click', () => visor.close());
    visor.addEventListener('click', (evento) => {
        if (evento.target === visor) {
            visor.close();
        }
    });
    visor.addEventListener('close', () => {
        imagen.removeAttribute('src');
        if (origen) {
            origen.focus();
        }
    });
});
