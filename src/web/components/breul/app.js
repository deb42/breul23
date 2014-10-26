"use strict";

/**
 * Bankbook Main Module
 * Includes sub pages modules and declares controllers, directives, ... needed for basic bankbook frame functionality
 **/

var breul = angular.module("breul", [     // declaration of bankbook (main) module
    "ngRoute",                                  // ngRoute directive for realizing routing
    "breul.api",                             // included bankbook modules
    "breul.common",
    "breul.patients",
    "breul.application",
    "breul.main"
]);

// create routing functionality on singleton $routeProvider and declare default route for non-existing sub pages

breul.config(['$routeProvider',
    function ($routeProvider) {
        // default route for non-existing routes
        $routeProvider.otherwise({
            redirectTo: "/"
        });
    }]);

breul.run(["Session", "$rootScope", "showLoginDialog", "$location", "isPatient", "isPhysician",
    function (Session, $rootScope, showLoginDialog, $location, isPatient, isPhysician) {


        var session = Session.get();
        // show modal for choosing advisor, if client and no advisor is set
        $rootScope.$watch(function () {
            return session.user;
        }, function () {
            /* jshint bitwise:false */
            var user = session.user;
        });

    }]);

breul.controller("NavbarCtrl", ["$scope", "$location", "Session", "isPhysician", "isPatient", "isAdmin", "AssignedPatients", "showLoginDialog",
    function ($scope, $location, Session, isPhysician, isPatient, isAdmin, AssignedPatients, showLoginDialog) {

        $scope.session = Session.get();
        $scope.isPhysician = isPhysician;
        $scope.isPatient = isPatient;
        $scope.isAdmin = isAdmin;

        $scope.assignedPatients = AssignedPatients.query();

        $scope.getNavActiveClass = function (path) {
            if (path === "/") {
                return $location.path() === "/" ? "active" : "";
            }
            if ($location.path().substr(0, path.length) === path) {
                return "navbar-element-selected";
            } else {
                return "";
            }
        };

        $scope.login = function () {
            showLoginDialog();
        };

        $scope.logout = function () {
            $location.path('/');
            Session.logout();
        };


    }]);


