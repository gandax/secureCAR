'use strict'

// Creation de l'app pour notre IHM
var carApp = angular.module('carApp', [
	'carData'
]);

var carData = angular.module('carData',[]);
// Angular controller pour notre IHM
carData.controller('carController', ['$scope', '$http',
	function($scope, $http){
        
        // constante pour calculer la commande de l'angle à envoyer
		const anglemax = 20;
        const anglemin = 10;
		
		// seuil de détection de diagnostic
		const threshold = 10;
		// seuil pour considérer que le gyroscope ne bouge pas
		const threshold_gyro = 5;

        // variable représentant l'ordre à envoyer au moteur (0 pour l'arrêt, 1 pour la marche arrière et 2 pour la marche avant)
		var motorCommand = 0;
        // varaible représentant la commande de l'angle (initialement au centre)
		var directionCommand = (anglemax+anglemin)/2;

        // codes des touches flèches
		var keyup = 38;
		var keydown = 40;
		var keyleft = 37;
		var keyright = 39;
        
        // booléens représentant l'appui sur les touches flèches
		var isKeyup = false;
		var isKeydown = false;
		var isKeyleft = false;
		var isKeyright = false;

		// valeur pour calculer l'écart de valeur entre les odomètres
		var oldLeftOdo = 0;
		var oldRightOdo = 0;
        
		$scope.init = function(){
            // initialisation des images des flèches en gris
			$("#uparrow").attr("src","static/img/arrow-up.png");
			$("#downarrow").attr("src","static/img/arrow-down.png");
			$("#rightarrow").attr("src","static/img/arrow-right.png");
			$("#leftarrow").attr("src","static/img/arrow-left.png");
            // initialisation des valeurs venant de la voiture
			$scope.left_odo = "";
			$scope.right_odo = "";
			$scope.potentiometer = "";
		};

        /***************************************************************
            Quand une touche est relaché
                - on met l'image correspondante à la flèche en gris
                - on met le booléen correspondant à false
                - si la touche est avant ou arrière, on envoie 0 comme
                    ordre sur les moteurs
        ****************************************************************/
		document.onkeyup = function(e){
			var keyCode = e.keyCode;
			if(keyCode==keyup && isKeyup){
				motorCommand = 0;
				sendCommands();
				isKeyup = false;
				$("#uparrow").attr("src","static/img/arrow-up.png");
			}else if(keyCode==keydown && isKeydown){
				motorCommand = 0;
				sendCommands();
				isKeydown =false;
				$("#downarrow").attr("src","static/img/arrow-down.png");
			}else if(keyCode==keyleft && isKeyleft){
				isKeyleft = false;
				$("#leftarrow").attr("src","static/img/arrow-left.png");
			}else if(keyCode==keyright && isKeyright){
				isKeyright =false;
				$("#rightarrow").attr("src","static/img/arrow-right.png");
			}

		}
        
        /**************************************************************
            Quand une touche est appuyé
                - on envoie l'ordre correspondant à la touche
                - dans le cas de gauche et droite, on vérifie que
                    l'angle reste entre les bornes min et max
        ***************************************************************/
		document.onkeydown = function(e){
			var keyCode = e.keyCode;
			if(keyCode==keyup && !isKeyup && !isKeydown){
				motorCommand = 2;
				sendCommands();
				isKeyup = true;
				$("#uparrow").attr("src","static/img/arrow-up-o.png");
			}else if(keyCode==keydown && !isKeydown && !isKeyup){
				motorCommand = 1;
				sendCommands();
				isKeydown = true;
				$("#downarrow").attr("src","static/img/arrow-down-o.png");
			}else if(keyCode==keyleft && !isKeyright){
                if(directionCommand<anglemax){
                    directionCommand++;
                    sendCommands();
                }
				isKeyleft = true;
				$("#leftarrow").attr("src","static/img/arrow-left-o.png");
			}else if(keyCode==keyright && !isKeyleft){
                if(directionCommand>anglemin){
                    directionCommand--;
				    sendCommands();
                }
				isKeyright = true;
				$("#rightarrow").attr("src","static/img/arrow-right-o.png");
			}
		}

		function sendCommands(){
            // Construction du json avec les commandes sur les moteurs et sur le volant
			var commands = {'motors' : motorCommand, 'direction' : directionCommand};
            // Envoi des sonnées au serveur
			$http({
			  method: 'POST',
			  url: '/data',
			  data: commands
			}).then(function successCallback(response) {
			    console.log("Commands sent");
			  }, function errorCallback(response) {
			    console.log("Error : " + response)
			});
		}

        // Récupération des données de la voiture
		function getData(){
			$http({
			  method: 'GET',
			  url: '/data',
			}).then(function successCallback(response) {
			    $scope.potentiometer = response.data.potentiometer;
			    $scope.left_odo = parseInt(response.data.left);
			    $scope.right_odo = parseInt(response.data.right);
                $scope.gyroscope = response.data.gyroscope+"°";
			    $scope.x = response.data.x.substr(0,4) + " m";
                $scope.y = response.data.y.substr(0,4) + " m";
                $scope.theta = response.data.theta.substr(0,4) + "°";
                $scope.gap = response.data.gap;
				$scope.derivative_gyro = response.data.derivative_gyro;
				// si on détecte une erreur
				if(Math.abs(parseInt($scope.gap)) > threshold){
					if($("#warning").has("img").length==0){
						// on indique que la voiture a rencontré un obstacle quand la valeur du gyroscope continue à évoluer
						if(Math.abs(parseInt($scope.derivative_gyro))>threshold_gyro){
							$("#warning").append("<img src=\"static/img/warning.png\" width=\"60px\" height=\"60px\"><p>The car has been pushed</p>");
						// sinon on indique que le voiture a rencontré un obstacle
						}else{
							$("#warning").append("<img src=\"static/img/warning.png\" width=\"60px\" height=\"60px\"><p>The car has hit an obstacle</p>");
						}
					}else{
						// si la voiture n'avance plus, on efface le warning
						if(motorCommand==0 && ($scope.left_odo-oldLeftOdo==0)&& ($scope.right_odo-oldRightOdo==0)){
							$("#warning").empty();
						}
					}
				}else{
					if($("#warning").has("img").length!=0){
						// si la voiture n'avance plus, on efface le warning
						if(motorCommand==0 && ($scope.left_odo-oldLeftOdo==0)&& ($scope.right_odo-oldRightOdo==0)){
							$("#warning").empty();
						}
					}
				}
				oldLeftOdo = $scope.left_odo;
				oldRightOdo = $scope.right_odo;
			  }, function errorCallback(response) {
			    console.log("Error : " + response)
			});
		}
        // Intervalle pour récupérer les données de la voiture (en ms)
		setInterval(getData, 500);
	}

]);
