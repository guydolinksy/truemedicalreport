import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {MatomoProvider, createInstance} from '@datapunt/matomo-tracker-react'
import Axios from "axios";
import * as Sentry from "@sentry/browser";
import { BrowserTracing } from "@sentry/tracing";

let instance = null;

// Initialize Sentry ASAP, before anything else
Axios.get("/api/tracing/config", {
    timeout: 250  // ms
}).then(response => {
    const sentryDsn = response.data.sentryDsn;
    const matomoUrlBase = response.data.matomoUrlBase;
    const matomoSiteId = response.data.matomoSiteId;

    if (sentryDsn) {
        console.log(`Got Sentry DSN ${sentryDsn}`)
        console.log("Initializing Sentry")
        
        Sentry.init({
            sentryDsn,
            integrations: [
                new BrowserTracing({
                    tracePropagationTargets: [`${window.location.host}/api`, /^\/api/],
                }),
            ],
            tracesSampleRate: 1.0,
        });
    }

    if(matomoUrlBase)
    {
        console.log(`Initializing matomo. Host: ${matomoUrlBase}, SiteId: ${matomoSiteId}`)

        instance = createInstance({
            urlBase: matomoUrlBase,
            siteId: matomoSiteId
        })
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
