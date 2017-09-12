'use strict';

var app = angular.module('KBase', ['ngRoute']);

app.factory('kbService', function($rootScope, $http, $q, $log) {
  $rootScope.status = 'Retrieving data...';
    return (
        $http.get('/questions')
            .then(function(data, status, headers, config) {
                $rootScope.questions = data;
                $rootScope.status = '';
            }));
});


/** MainCtrl has the ability to search for questions, or ask one */
app.controller('MainCtrl', function($http, $rootScope, $scope) {
    console.log('creating search ');
    $scope.search = function () {
        console.log('search ', $scope.query);
        ($http.get('questions', {q: $scope.query})
         .then(function (response) {
             console.log('Got response', response.data);
             $scope.questions = response.data.questions;
             if (!$scope.questions) {
                 $rootScope.status = "No answers found";
             }
         }));
    }
    $scope.questions = [];
});

/** AskCtrl Controls the form to ask questions, and submitting them */
app.controller('AskCtrl', function($http, $location, $rootScope, $scope) {
    $scope.submitQuestion = function () {
        console.log($scope.question, $scope.answer);
        ($http.post('questions', {q: $scope.question, a: $scope.answer})
         .then(function (response) {
             console.log('Got response', response);
             $scope.questions = response.data.questions;
             if (!$scope.questions) {
                 $rootScope.status = "No answers found";
             }
             $location.path('#!/');
             console.log('Changed location');
         }).catch(function (err) {
             console.log('err', err);
         }));
    };
    $scope.questions = [];
});


app.config(function($routeProvider) {
  $routeProvider.when('/', {
      templateUrl: 'partials/main.html',
      resolve    : { 'kbService': 'kbService' },
  }).when('/ask', {
      controller : 'AskCtrl',
      templateUrl: 'partials/ask.html',
  }).when('/edit/:id', {
    controller : 'EditCtrl',
    templateUrl: 'partials/edit.html',
    resolve    : { 'kbService': 'kbService' },
  }).otherwise({
    redirectTo : '/'
  });
});
