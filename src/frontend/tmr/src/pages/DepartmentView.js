import React, {useEffect, useState} from 'react';
import Axios from 'axios';
import {Row, Col, Card} from 'antd';
import {Department} from "../components/Department";

export const DEPARTMENT_URL = '/'
export const DepartmentView = () => {
    return <div style={{padding: 16}}>
            <Department/>
    </div>
}