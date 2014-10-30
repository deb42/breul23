"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var barCharge = angular.module("breul.barCharge", [
    "ngRoute",
    "breul.barCharge"
]);

barCharge.controller("barChargeCtrl", ["$scope", "Session", "Items", "SoldItemBar", function ($scope, Session, Items, SoldItemBar) {
    $scope.session = Session.get();
    $scope.items = Items.query();
    $scope.amount = 1;


    $scope.$watch("session.user", function () {
        var soldItemBar = new SoldItemBar({
            resident: $scope.session.user
        });

    });

    $scope.add = function (item, amount) {
        console.log(item, amount);
        var soldItemBar = new SoldItemBar({
            bar_charge_id: 1,
            item_id: item.id,
            amount: amount
        })
        soldItemBar.$save();
        $scope.amount = 1;

    }

}]);

barCharge.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/barCharge', {
        controller: ("test", ["$http", "$location", function ($http, $location) {
            $http.get("/api/session").success(

                function (session) {
                    console.log(session);
                    console.log(session.bar_charge.barCharge.resident_id === session.user.id);
                    if(session.bar_charge.barCharge.resident_id !== session.user.id){
                        alert("nicht authorisiert");
                        $location.path("/");

                    }
                }

            );
        }]),
        templateUrl: '/components/breul/bar-charge/bar-charge.html'
    });
}]);