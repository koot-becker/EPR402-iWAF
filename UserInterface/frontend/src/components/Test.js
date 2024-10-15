import React, { Component } from 'react';
import {
    Button,
    Modal,
    ModalHeader,
    ModalBody,
    ModalFooter,
    Form,
    FormGroup,
    Input,
    Label,
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
                    <div className="row">
                        <div className="col-sm-4">
                            <h5>Choose Balanced Test:</h5>
                            <div className="button-container">
                                <Button
                                color="primary"
                                onClick={() => {}}
                                >
                                    Test 1
                                </Button>
                                <Button
                                color="primary"
                                onClick={() => {}}
                                >
                                    Test 2
                                </Button>
                                <Button
                                color="primary"
                                onClick={() => {}}
                                >
                                    Test 3
                                </Button>
                            </div>
                            <p>Average Time Delay [%]: </p>
                            <p>Total: </p>
                            <p>True Positive Rate: </p>
                            <p>False Positive Rate: </p>
                            <p>True Negative Rate: </p>
                            <p>False Negative Rate: </p>
                        </div>
                        <div className="col-sm-4">
                            <h5>Choose Conventional Test:</h5>
                            <div className="button-container">
                            <Button
                                color="primary"
                                onClick={() => {}}
                                >
                                    Test 1
                                </Button>
                                <Button
                                color="primary"
                                onClick={() => {}}
                                >
                                    Test 2
                                </Button>
                                <Button
                                color="primary"
                                onClick={() => {}}
                                >
                                    Test 3
                                </Button>
                            </div>
                            <p>Average Time Delay [%]: </p>
                            <p>Total: </p>
                            <p>True Positive Rate: </p>
                            <p>False Positive Rate: </p>
                            <p>True Negative Rate: </p>
                            <p>False Negative Rate: </p>
                        </div>
                        <div className="col-sm-4">
                            <h5>Choose Unconventional Test:</h5>
                            <div className="button-container">
                                <Button
                                color="primary"
                                onClick={() => {}}
                                >
                                    Test 1
                                </Button>
                                <Button
                                color="primary"
                                onClick={() => {}}
                                >
                                    Test 2
                                </Button>
                                <Button
                                color="primary"
                                onClick={() => {}}
                                >
                                    Test 3
                                </Button>
                            </div>
                            <p>Average Time Delay [%]: </p>
                            <p>Total: </p>
                            <p>True Positive Rate: </p>
                            <p>False Positive Rate: </p>
                            <p>True Negative Rate: </p>
                            <p>False Negative Rate: </p>
                        </div>
                    </div>
                    <div className="row plots-container">
                        <div className="col-sm-4 plot-container">
                            <h5>Balanced Efficacy</h5>
                            <ResponsiveContainer width="90%" height={300}>
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
                                    x: 50, 
                                    y: 50
                                    }]} 
                                    fill="#8884d8" 
                                />
                                </ScatterChart>
                            </ResponsiveContainer>
                        </div>
                        <div className="col-sm-4 plot-container">
                            <h5>Conventional Efficacy</h5>
                            <ResponsiveContainer width="90%" height={300}>
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
                                    x: 50, 
                                    y: 50
                                    }]} 
                                    fill="#8884d8" 
                                />
                                </ScatterChart>
                            </ResponsiveContainer>
                        </div>
                        <div className="col-sm-4 plot-container">
                            <h5>Unconventional Efficacy</h5>
                            <ResponsiveContainer width="90%" height={300}>
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
                                    x: 50, 
                                    y: 50
                                    }]} 
                                    fill="#8884d8" 
                                />
                                </ScatterChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </FormGroup>
                </Form>
                </ModalBody>
            </Modal>
        );
    }

}