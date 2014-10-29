"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var barCharge = angular.module("breul.barCharge", [
    "ngRoute",
    "breul.barCharge"
]);

barCharge.controller("announcementsCtrl", ["$scope", "Session", "Announcements", function ($scope, Session, Announcements) {
    $scope.session = Session.get();

    $scope.$watch("session.user", function () {
        $scope.announcements = Announcements.query();
    });

}]);

barCharge.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/barCharge', {
        templateUrl: '/components/breul/bar-charge/bar-charge.html'
    });
}]);