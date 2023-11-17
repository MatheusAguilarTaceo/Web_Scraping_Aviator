function site() {
    let iframe_house = document.querySelector('iframe');
    console.log(iframe_house)
    // iframe_house.forEach(value =>{
    //     console.log(value)
    // })

    iframe_house = iframe_house.contentWindow
    iframe_house = iframe_house.document
    let iframe_jogo = iframe_house.querySelector('iframe')
    console.log(iframe_jogo)
}

site();


function serverJogo(){
    let teste = document.querySelector('div');
    console.log(teste);
}
serverJogo();