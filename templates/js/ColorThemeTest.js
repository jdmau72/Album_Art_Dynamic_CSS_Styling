let color1 = [0, 0, 0];
let color2 = [255, 255, 255];

// $("albumBanner").css({background: linear-gradient(to bottom, color1 color2)})
$("albumBanner").css("background", `linear-gradient(to bottom, rgb(${color1[0]}, ${color1[1]}, ${color1[2]}), rgb(${color2[0]},${color2[1]},${color2[2]}))`);

$("TEST").innerText = "TEST";
