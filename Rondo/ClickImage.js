// Univerzální modul pro opakované hledání a klikání na obrázek
// Název obrázku se předává z UI.Vision přes proměnnou imageName

const imageName = uiv.getVar('imageName');   // parametr z makra
const maxKliknuti = 100;
let pocet = 0;

while (pocet < maxKliknuti) {

  const objekt = uiv.findImage(imageName, {
    scope: 'desktop',
    minScore: 0.69,
    required: false,
    timeout: 2
  });

  if (!objekt) {
    break;
  }

  uiv.desktop.click(objekt);
  pocet++;
}

if (pocet === 0) {
  throw new Error(`${imageName} nebyl nalezen; nebylo provedeno žádné kliknutí.`);
}

if (pocet === maxKliknuti) {
  throw new Error(`Dosažen bezpečnostní limit ${maxKliknuti} kliknutí; ověřte stav hry.`);
}

uiv.log(`Kliknuto na ${pocet} objektů podle ${imageName}.`, 'green');
