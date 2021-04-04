import React from 'react';
import ReactDOM from 'react-dom';
import List from './containers/List';
import 'bootstrap/dist/css/bootstrap.min.css';

const App = () => {
    return (
        <div className = 'container-fluid' >
            < nav className = 'navbar sticky-top navbar-light bg-dark' > 
                < h1 className = 'navbar-brand text-light' >movieList</h1>
            </nav >
            <List /> 
        </div>
    );
};

ReactDOM.render( < App / > , document.getElementById('root'));