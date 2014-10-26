var common = angular.module("formmanagement.common", [
    "ngRoute",
    "formmanagement.api"
]);


common.factory('showSingUpDialog', ['$modal', '$http', 'Session', 'Patient',
    function ($modal, $http, Session, Patient) {

        var NewPatientCtrl = function ($scope, $modalInstance, $location) {
            $scope.patient = {surname: "", forename: "", gender: "", birthday: "", username: "", password: ""};

            $scope.save = function () {
                $scope.forename = $scope.surname = $scope.gender = $scope.birthday = $scope.username = $scope.usernameExists = $scope.password = $scope.passwordUnequal = false;
                if (!$scope.patient.forename) {
                    $scope.forename = true;
                } else if (!$scope.patient.surname) {
                    $scope.surname = true;
                } else if (!$scope.patient.birthday) {
                    $scope.birthday = true;
                } else if (!$scope.patient.gender) {
                    $scope.gender = true;
                } else if (!$scope.patient.username) {
                    $scope.username = true;
                } else if (!$scope.patient.password) {
                    $scope.password = true;
                } else if ($scope.patient.comparePassword !== $scope.patient.password) {
                    $scope.passwordUnequal = true;
                } else {

                    var newPatient = new Patient({
                        username: $scope.patient.username,
                        pw_hash: $scope.patient.password,
                        name: $scope.patient.forename + " " + $scope.patient.surname,
                        birthday: $scope.patient.birthday,
                        gender:  $scope.patient.gender,
                        physician_id: 0
                    });

                    var path = 'api/users/' + $scope.patient.username;
                    $http.get(path)
                        .error(function () {
                            Session.signup(newPatient).success(function () {
                                $modalInstance.close();
                                $location.path('/questionnaire');
                            });
                        })
                        .success(function () {
                            $scope.usernameExists = true;
                        });
                }
            };

            $scope.back = function () {
                $modalInstance.close();
                window.location.reload();
            };


        };

        return function showSingUpDialog() {
            $modal.open({
                controller: NewPatientCtrl,
                templateUrl: '/components/formmanagement/login/new-patient.html',
                keyboard: false,
                backdrop: "static"
            });
        };

    }]);

common.directive('picture', [function () {
    return {
        scope: {
            source: "=", // user object
            title: "=?"
        },
        restrict: "E",
        link: function (scope, element, attrs) {
            // set watcher for user object (see options page)

            scope.$watch("source", function (image) {
                if (image) {
                    scope.url = "/api/files/" + image;
                } else {
                    scope.url = "";
                }
                console.log(image)
                console.log(scope.url);
            });
            scope.getTitle = function () {
                if (scope.title) {
                    return scope.title;
                } else if (scope.user) {
                    return scope.user.name;
                } else {
                    return "";
                }
            };
        },
        template: '<img class="img-rounded profile-picture" ng-src="{{ url }}" title="{{ getTitle() }}" />'
    };
}]);

