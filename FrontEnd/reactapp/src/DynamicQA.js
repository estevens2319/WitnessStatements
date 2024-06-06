
import React, { useState } from 'react';
import './Statements.css';
import { usePromiseTracker } from "react-promise-tracker";
import { TextField, Button, Typography, CircularProgress } from '@mui/material';

import axios from "axios";
import { trackPromise } from 'react-promise-tracker';

const LoadingIndicator = () => {    
    const { promiseInProgress } = usePromiseTracker();
    return (
        promiseInProgress && <CircularProgress color="primary" />
    );
}

function DynamicQA() {
    const [text, setText] = useState('');
    const [crime, setCrime] = useState('');
    const [responses, setResponses] = useState([]);

    const handleSubmit = () => {
        trackPromise(
            axios.post("/DynamicQA", { text, crime })
                .then((response) => setResponses(response.data))
                .catch((error) => console.error('Error:', error))
        );
    };

    return (
        <div className="InteractiveQA" style={{ padding: '20px', maxWidth: '600px', margin: 'auto', textAlign: 'center' }}>
            <Typography variant="h4" gutterBottom>
                FAQ's
            </Typography>

            <TextField 
                label="Enter Case Number" 
                variant="outlined" 
                value={text} 
                onChange={(e) => setText(e.target.value)} 
                fullWidth 
                margin="normal"
                style={{ marginBottom: '15px' }}
            />

            <TextField 
                label="What was the crime?" 
                variant="outlined" 
                value={crime} 
                onChange={(e) => setCrime(e.target.value)} 
                fullWidth 
                margin="normal"
                style={{ marginBottom: '15px' }}
            />

            <Button variant="contained" color="primary" onClick={handleSubmit}>
                Submit
            </Button>

            <div style={{ marginTop: '20px', textAlign: 'left' }}>
                {responses.map((qa, index) => (
                    <div key={index} style={{ marginBottom: '15px' }}>
                        <Typography variant="body1" style={{ fontWeight: 'bold' }}>
                            Question: {qa.question}
                        </Typography>
                        <Typography variant="body1">
                            Answer: {qa.answer}
                        </Typography>
                    </div>
                ))}
            </div>

            <LoadingIndicator />
        </div>
    );
}

export default DynamicQA;
