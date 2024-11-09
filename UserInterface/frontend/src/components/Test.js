import axios from 'axios';
import React, { Component } from 'react';
import {
    Button,
    ButtonGroup,
    Modal,
    ModalHeader,
    ModalBody,
    ModalFooter,
    Form,
    FormGroup,
  } from "reactstrap";
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';


export default class CustomTest extends Component {
    constructor(props) {
      super(props);
      this.state = {
        activeItem: this.props.activeItem,
      };
    }

    handleChange = (e) => {
        let { name, value } = e.target;

        if (e.target.type === "checkbox") {
            value = e.target.checked;
        }

        const activeItem = { ...this.state.activeItem, [name]: value };

        this.setState({ activeItem });
    };

    render() {
        const { toggle, onSave } = this.props;

        return (
            <Modal isOpen={true} toggle={toggle} size='xl'>
            <ModalHeader toggle={toggle}>WAF Testing</ModalHeader>
            <ModalBody>
            <Form>
            <FormGroup>
            <h5>Results:</h5>
            <div className='row'>
            <div className='col-md-4'>
                <div className='waf-container'>
                <div className="test-container">
                <h5>Overall Balanced Efficacy</h5>
                <div className="plot-container">
                <ButtonGroup>
                    <Button
                    color="primary"
                    onClick={() => {
                        const activeItem = { 
                            ...this.state.activeItem, 
                            results: { 
                            ...this.state.activeItem.results, 
                            balanced: {
                                time: this.state.activeItem.results.balanced.time,
                                tnr: (3*this.state.activeItem.results.conventional.tnr + this.state.activeItem.results.unconventional.tnr) / 4, 
                                tpr: (3*this.state.activeItem.results.conventional.tpr + this.state.activeItem.results.unconventional.tpr) / 4,
                            }}};
                        this.setState({ activeItem });
                    }}
                    style={{ marginBottom: '10px', borderRadius: '5px', marginRight: '10px' }}
                    >
                    Test Combined
                    </Button>
                </ButtonGroup>
                <h6>TP vs. TN</h6>
                <ResponsiveContainer width="90%" height={250}>
                    <ScatterChart
                    margin={{
                    top: 20,
                    right: 20,
                    bottom: 20,
                    left: 20,
                    }}
                    >
                    <CartesianGrid />
                    <XAxis type="number" dataKey="x" name="True Negative" unit="%" domain={[0, 100]} label={{ value: 'True Negative', angle: 0, position: 'insideBottom', offset: -10 }} />
                    <YAxis type="number" dataKey="y" name="True Positive" unit="%" domain={[0, 100]} label={{ value: 'True Positive', angle: -90, position: 'insideLeft', offset: 0 }} />
                    <ReferenceLine  y={90} stroke="red" strokeDasharray="4 4" />
                    <ReferenceLine x={90} stroke="red" strokeDasharray="4 4" />
                    <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                    <Scatter 
                    name="Efficacy"
                    data={[{
                    x: this.state.activeItem.results.balanced.tnr, 
                    y: this.state.activeItem.results.balanced.tpr
                    }]} 
                    fill="#8884d8" 
                    />
                    </ScatterChart>
                </ResponsiveContainer>
                </div>
                </div>
                </div>
            </div>
            <div className='col-md-4'>
                <div className="test-container">
                <h5>Conventional Efficacy</h5>
                <div className="plot-container">
                <ButtonGroup>
                    <Button
                    color="primary"
                    onClick={() => {
                    const blocked_ips = [...this.state.activeItem.rules.blocked_ips, ""];
                    const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_ips } };
                    this.setState({ activeItem });
                    axios
                    .post('/api/wafs/get_conventional_results/', this.state.activeItem)
                    .then((res) => {
                        console.log(res.data);
                        const activeItem = { 
                        ...this.state.activeItem, 
                        results: { 
                        ...this.state.activeItem.results, 
                        conventional: res.data
                        } 
                        };
                        this.setState({ activeItem });
                    })
                    }}
                    style={{ marginBottom: '10px', borderRadius: '5px', marginRight: '10px' }}
                    >
                    Test Conventional
                    </Button>
                </ButtonGroup>
                <h6>TP vs. TN</h6>
                <ResponsiveContainer width="90%" height={250}>
                <ScatterChart
                margin={{
                top: 20,
                right: 20,
                bottom: 20,
                left: 20,
                }}
                >
                <CartesianGrid />
                <XAxis type="number" dataKey="x" name="True Negative" unit="%" domain={[0, 100]} label={{ value: 'True Negative', angle: 0, position: 'insideBottom', offset: -10 }} />
                <YAxis type="number" dataKey="y" name="True Positive" unit="%" domain={[0, 100]} label={{ value: 'True Positive', angle: -90, position: 'insideLeft', offset: 0 }} />
                <ReferenceLine  y={95} stroke="red" strokeDasharray="4 4" />
                <ReferenceLine x={95} stroke="red" strokeDasharray="4 4" />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                <Scatter 
                    name="Efficacy"
                    data={[{
                    x: this.state.activeItem.results.conventional.tnr, 
                    y: this.state.activeItem.results.conventional.tpr
                    }]} 
                    fill="#8884d8" 
                />
                </ScatterChart>
                </ResponsiveContainer>
                </div>
                </div>
            </div>
            <div className='col-md-4'>
                <div className="test-container">
                <h5>Unconventional Efficacy</h5>
                <div className="plot-container">
                <ButtonGroup>
                    <Button
                    color="primary"
                    onClick={() => {
                    const blocked_ips = [...this.state.activeItem.rules.blocked_ips, ""];
                    const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_ips } };
                    this.setState({ activeItem });
                    axios
                    .post('/api/wafs/get_unconventional_results/', this.state.activeItem)
                    .then((res) => {
                        console.log(res.data);
                        const activeItem = {
                        ...this.state.activeItem, 
                        results: { 
                        ...this.state.activeItem.results, 
                        unconventional: res.data 
                        } 
                        };
                        this.setState({ activeItem });
                    })
                    }}
                    style={{ marginBottom: '10px', borderRadius: '5px', marginRight: '10px' }}
                    >
                    Test Unconventional
                    </Button>
                </ButtonGroup>
                <h6>TP vs. TN</h6>
                <ResponsiveContainer width="95%" height={250}>
                <ScatterChart
                margin={{
                top: 20,
                right: 20,
                bottom: 20,
                left: 20,
                }}
                >
                <CartesianGrid />
                <XAxis type="number" dataKey="x" name="True Negative" unit="%" domain={[0, 100]} label={{ value: 'True Negative', position: 'insideBottom', offset: -10 }} />
                <YAxis type="number" dataKey="y" name="True Positive" unit="%" domain={[0, 100]} label={{ value: 'True Positive', angle: -90, position: 'insideLeft', offset: 0 }} />
                <ReferenceLine x={75} stroke="red" strokeDasharray="4 4" />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                <Scatter 
                    name="Efficacy"
                    data={[{
                    x: this.state.activeItem.results.unconventional.tnr, 
                    y: this.state.activeItem.results.unconventional.tpr
                    }]} 
                    fill="#8884d8" 
                />
                </ScatterChart>
                </ResponsiveContainer>
                </div>
                </div>
            </div>
            </div>
            </FormGroup>
            </Form>
            </ModalBody>
            <ModalFooter>
                <Button
                color="success"
                onClick={() => onSave(this.state.activeItem)}
                >
                Save
                </Button>
            </ModalFooter>
            </Modal>
        );
    }

}