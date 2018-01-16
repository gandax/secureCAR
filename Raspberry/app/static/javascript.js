'use strict'

var carApp = angular.module('carApp', [
	'carData'
]);

var carData = angular.module('carData',[]);
carData.controller('carController', ['$scope', '$http',
	function($scope, $http){


		const anglemax = 20;
        const anglemin = 10;

		var motorCommand = 0;
		var directionCommand = (anglemax+anglemin)/2;

		var keyup = 38;
		var keydown = 40;
		var keyleft = 37;
		var keyright = 39;
		var isKeyup = false;
		var isKeydown = false;
		var isKeyleft = false;
		var isKeyright =false;


		$scope.init = function(){
			$("#uparrow").attr("src","static/img/arrow-up.png");
			$("#downarrow").attr("src","static/img/arrow-down.png");
			$("#rightarrow").attr("src","static/img/arrow-right.png");
			$("#leftarrow").attr("src","static/img/arrow-left.png");
			$scope.left_odo = "";
			$scope.right_odo = "";
			$scope.potentiometer = "";
		};

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
			var commands = {'motors' : motorCommand, 'direction' : directionCommand};
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

		function getData(){
			$http({
			  method: 'GET',
			  url: '/data',
			}).then(function successCallback(response) {
			    $scope.potentiometer = response.data.potentiometer+"°";
			    $scope.left_odo = response.data.left+"°";
			    $scope.right_odo = response.data.right+"°";
			    $scope.x = response.data.x.substr(0,4) + " m";
                $scope.y = response.data.y.substr(0,4) + " m";
                $scope.theta = response.data.theta.substr(0,4) + "°";
			  }, function errorCallback(response) {
			    console.log("Error : " + response)
			});
		}

		setInterval(getData, 500);
	}

]);
