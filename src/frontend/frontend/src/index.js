import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {MatomoProvider, createInstance} from '@datapunt/matomo-tracker-react'
import Axios from "axios";
import * as Sentry from "@sentry/browser";
import { BrowserTracing } from "@sentry/tracing";

const instance = createInstance({
    urlBase: 'http://localhost:8090/',
    siteId: 1
})

// Intialize Sentry ASAP, before anything else
Axios.get("/api/tracing/dsn", {
    timeout: 250  // ms
}).then(response => {
    const dsn = response.data;
    console.log(`Got Sentry DSN ${dsn}`)

    if (dsn) {
        console.log("Initializing Sentry")
        
        Sentry.init({
            dsn,
            integrations: [
                new BrowserTracing({
                    tracePropagationTargets: [`${window.location.host}/api`, /^\/api/],
                }),
            ],
        });
    }
}).finally(() => {
    ReactDOM.render(
        <React.StrictMode>
            <MatomoProvider value={instance}>
                <App />
            </MatomoProvider>
        </React.StrictMode>,
        document.getElementById('root')
    );
})

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
