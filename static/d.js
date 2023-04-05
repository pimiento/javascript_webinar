var roll = function () {
    res=(Math.floor(Math.random() * 6))+1;
    document.getElementById('die-num').innerHTML=res;
    f_color_r=(Math.floor(Math.random()*0xF0) + 0xF);
    f_color_g=(Math.floor(Math.random()*0xF0)) + 0xF;
    f_color_b=(Math.floor(Math.random()*0xF0) + 0xF);
    document.getElementById('die-num').style.color='#'+f_color_r+f_color_g+f_color_b;
};
