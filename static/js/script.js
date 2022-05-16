// Récupération des blocs
var mainMenu = document.querySelector("#menu");
var burgerMenu = document.querySelector("#menu-burger");

/*===============================*/
/*=== Clic sur le menu burger ===*/
/*===============================*/
// Vérifie si l'événement touchstart existe et est le premier déclenché
var clickedEvent = "click"; // Au clic si "touchstart" n'est pas détecté
window.addEventListener('touchstart', function detectTouch() {
	clickedEvent = "touchstart"; // Transforme l'événement en "touchstart"
	window.removeEventListener('touchstart', detectTouch, false);
}, false);

// Créé un "toggle class" en Javascrit natif (compatible partout)
burgerMenu.addEventListener(clickedEvent, function (evt) {
	console.log(clickedEvent);
	// Modification du menu burger
	if (!this.getAttribute("class")) {
		this.setAttribute("class", "clicked");
	} else {
		this.removeAttribute("class");
	}
	// Variante avec x.classList (ou DOMTokenList), pas 100% compatible avant IE 11...
	// burgerMenu.classList.toggle("clicked");

	// Créé l'effet pour le menu slide (compatible partout)
	if (mainMenu.getAttribute("class") != "visible") {
		mainMenu.setAttribute("class", "visible");
	} else {
		mainMenu.setAttribute("class", "invisible");
	}
}, false);

/*===============================*/
/*=== Swipe avec Touch Events ===*/
/*===============================*/
// Si l'écran est plus petit que "x" pixels (optionnel) // 1024px ici
if (screen.width <= 1024) {
	var startX = 0; // Position de départ
	var distance = 100; // 100 px de swipe pour afficher le menu

	// Au premier point de contact
	window.addEventListener("touchstart", function (evt) {
		// Récupère les "touches" effectuées
		var touches = evt.changedTouches[0];
		startX = touches.pageX;
		between = 0;
	}, false);

	// Quand les points de contact sont en mouvement
	window.addEventListener("touchmove", function (evt) {
		// Limite les effets de bord avec le tactile...
		evt.preventDefault();
		evt.stopPropagation();
	}, false);

	// Quand le contact s'arrête
	window.addEventListener("touchend", function (evt) {
		var touches = evt.changedTouches[0];
		var between = touches.pageX - startX;

		// Détection de la direction
		if (between > 0) {
			var orientation = "ltr";
		} else {
			var orientation = "rtl";
		}

		// Modification du menu burger
		if (Math.abs(between) >= distance && orientation == "ltr" && mainMenu.getAttribute("class") != "visible") {
			burgerMenu.setAttribute("class", "clicked");
		}
		if (Math.abs(between) >= distance && orientation == "rtl" && mainMenu.getAttribute("class") != "invisible") {
			burgerMenu.removeAttribute("class");
		}

		// Créé l'effet pour le menu slide (compatible partout)
		if (Math.abs(between) >= distance && orientation == "ltr" && mainMenu.getAttribute("class") != "visible") {
			mainMenu.setAttribute("class", "visible");
		}
		if (Math.abs(between) >= distance && orientation == "rtl" && mainMenu.getAttribute("class") != "invisible") {
			mainMenu.setAttribute("class", "invisible");
		}
	}, false);
}


let color_stock = ""

function popup(page, titre, largeur, hauteur, options) {
    if (options == null) {
        options = 'resizable=no, location=no, status=no, scrollbars=no, menubar=no, toolbar=no';
    }
    // document.body.style.backgroundColor = "#000";
    // document.body.style.opacity = "0.4";
    var top = (screen.height - hauteur) / 2 - 30;
    var left = (screen.width - largeur) / 2;
    var w = window.open(page, titre, `top=${top},left=${left},width=${largeur},height=${hauteur},${options}`);
    w.focus();
}


function over_color(id) {
    color_stock = document.getElementById(id).style.backgroundColor;
    document.getElementById(id).style.backgroundColor = "#999999";
}


function out_color(id) {
    document.getElementById(id).style.backgroundColor = color_stock;
}


$(document).ready(function () {

	// CALENDRIER POUR LES SAISIES DE DATE
	$.datepicker.regional['fr'] = {
		closeText: 'Fermer',
		prevText: '&#x3c;Préc',
		nextText: 'Suiv&#x3e;',
		currentText: 'Aujourd\'hui',
		monthNames: ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin',
			'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre'
		],
		monthNamesShort: ['Jan', 'Fev', 'Mar', 'Avr', 'Mai', 'Jun',
			'Jul', 'Aou', 'Sep', 'Oct', 'Nov', 'Dec'
		],
		dayNames: ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'],
		dayNamesShort: ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'],
		dayNamesMin: ['Di', 'Lu', 'Ma', 'Me', 'Je', 'Ve', 'Sa'],
		weekHeader: 'Sm',
		dateFormat: 'dd/mm/yy',
		firstDay: 1,
		isRTL: false,
		showMonthAfterYear: false,
		yearSuffix: '',
		minDate: '-30Y',
		maxDate: '+10Y',
		numberOfMonths: 1,
		showButtonPanel: true,
		changeMonth: true,
		changeYear: true
	};
	$.datepicker.setDefaults($.datepicker.regional['fr']);

	$("#id_date_debut").datepicker({
		showOn: "button",
		buttonImage: "/static/images/calendrier20.png",
	});

	$("#id_date_fin").datepicker({
		showOn: "button",
		buttonImage: "/static/images/calendrier20.png",
	});

})