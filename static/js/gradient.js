gradientPercent = 0;
gradientPercentStep = 0.05;
gradientVelocity = 0;
gradientInterval = null;
pg = null

function setRedBackground(page) {
    pg = page;
    if (gradientPercent != 0) {
        gradientPercent = 1.0 - gradientPercentStep;
        gradientVelocity = -gradientPercentStep;
        startGradientInterval();
    }
}

function setGreenBackground(page) {
    pg = page;
    if (gradientPercent != 1) {
        gradientPercent = gradientPercentStep;
        gradientVelocity = gradientPercentStep;
        startGradientInterval();
    }
}

function startGradientInterval() {
    gradientInterval = window.setInterval(function() {
        setGradientStyle(pg);
    }, 30);
}

function setGradientStyle(target) {
    var color;
    if (gradientPercent == 0) {
        color = "red";
        window.clearInterval(gradientInterval);
    } else if (gradientPercent == 1) {
        color = "green";
        window.clearInterval(gradientInterval);
    } else {
        // create gradient color
        color = "#"
        var red = Math.floor((1 - gradientPercent) * 255);
        if (red < 16) {
            color += "0";
        }
        color += red.toString(16);
        var green = Math.floor((gradientPercent) * 128);
        if (green < 16) {
            color += "0";
        }
        color += green.toString(16);
        color += "00";

        // step the gradient
        gradientPercent += gradientVelocity;
        // ensure bounds of gradient
        gradientPercent = Math.min(1, Math.max(0, gradientPercent));
    }
    target.style.background = "linear-gradient(to bottom right, " + color + ", yellow)";
}












//            __              __              
//           /  \            /  \      
//           \  /            \  /
//            --              --
//
//      __            /              __
//       |           /_              | 
//        \                         /
//         ==                     ==
//         |   ------------------  |
//           \ |  |  |  |  |  | | /
//             ------------------ 





