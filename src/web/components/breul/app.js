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
    "breul.main",
    "breul.intern",
    "breul.announcements",
    "breul.barCharge"
]);

// create routing functionality on singleton $routeProvider and declare default route for non-existing sub pages

breul.config(['$routeProvider',
    function ($routeProvider) {
        // default route for non-existing routes
        $routeProvider.otherwise({
            redirectTo: "/"
        });
    }]);

breul.run(["Session", "$rootScope", "showLoginDialog", "$location", "BarCharge",
    function (Session, $rootScope, showLoginDialog, $location,BarCharge) {


        var session = Session.get();
        // show modal for choosing advisor, if client and no advisor is set
        $rootScope.$watch(function () {
            return session.user;
        }, function () {
            /* jshint bitwise:false */
            var user = session.user;
        });

        $rootScope.$on('$routeChangeStart', function (next, current) {
           console.log($location.path())
            if($location.path()=== "/barCharge"){
               /* BarCharge.setUserAuthenticated(session.bar_charge.barCharge.resident_id === session.user.id)
                if(session.bar_charge.barCharge.resident_id === session.user.id){
                    alert("allowed")
                }
                else{
                    alert("NOT ALLOWED")
                }*/
                console.log(BarCharge.getUserAuthenticated())

            }
        });

    }]);

breul.controller("NavbarCtrl", ["$scope", "$location", "Session", "showLoginDialog",
    function ($scope, $location, Session, showLoginDialog) {

        $scope.session = Session.get();

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


