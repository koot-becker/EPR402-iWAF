import React, { Component } from 'react';
import {
    Button,
    ButtonGroup,
    Modal,
    ModalHeader,
    ModalBody,
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
        const { toggle } = this.props;

        return (
            <Modal isOpen={true} toggle={toggle} size='xl'>
                <ModalHeader toggle={toggle}>WAF Testing</ModalHeader>
                <ModalBody>
                <Form>
                <div className='test-container' style={{ marginBottom: '10px', paddingBottom: '0px'}}>
                    <h5>Choose Configuration:</h5>
                    <div className='button-container' style={{ gap: '20px' }}>
                        <FormGroup className='test-container'>
                            <legend>Choose Dataset: </legend>
                            <FormGroup check>
                                <Label check>
                                <Input type="radio" name="radio2" />{' '}
                                CSIC
                                </Label>
                            </FormGroup>
                            <FormGroup check>
                                <Label check>
                                <Input type="radio" name="radio2" />{' '}
                                ECML
                                </Label>
                            </FormGroup>
                            <FormGroup check disabled>
                                <Label check>
                                <Input type="radio" name="radio2" />{' '}
                                Combined
                                </Label>
                            </FormGroup>
                        </FormGroup>
                        <FormGroup className='test-container'>
                            <legend>Choose Split: </legend>
                            <FormGroup check>
                                <Label check>
                                <Input type="radio" name="radio1" />{' '}
                                25/75
                                </Label>
                            </FormGroup>
                            <FormGroup check>
                                <Label check>
                                <Input type="radio" name="radio1" />{' '}
                                50/50
                                </Label>
                            </FormGroup>
                            <FormGroup check>
                                <Label check>
                                <Input type="radio" name="radio1" />{' '}
                                75/25
                                </Label>
                            </FormGroup>
                        </FormGroup>
                        <FormGroup className='test-container'>
                            <ButtonGroup vertical>
                                <Button
                                color="primary"
                                onClick={() => {
                                    const blocked_ips = [...this.state.activeItem.rules.blocked_ips, ""];
                                    const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_ips } };
                                    this.setState({ activeItem });
                                }}
                                style={{ marginBottom: '10px', borderRadius: '5px' }}
                                >
                                    Test Balanced
                                </Button>
                                <Button
                                color="primary"
                                onClick={() => {
                                    const blocked_ips = [...this.state.activeItem.rules.blocked_ips, ""];
                                    const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_ips } };
                                    this.setState({ activeItem });
                                }}
                                style={{ marginBottom: '10px', borderRadius: '5px' }}
                                >
                                    Test Conventional
                                </Button>
                                <Button
                                color="primary"
                                onClick={() => {
                                    const blocked_ips = [...this.state.activeItem.rules.blocked_ips, ""];
                                    const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_ips } };
                                    this.setState({ activeItem });
                                }}
                                style={{ borderRadius: '5px' }}
                                >
                                    Test Unconventional
                                </Button>
                            </ButtonGroup>
                        </FormGroup>
                    </div>
                </div>
                <FormGroup>
                    <h5>Results:</h5>
                    <div className='row'>
                        <div className='col-md-4'>
                            <div className='waf-container'>
                                <div className="test-container">
                                    <h5>Balanced Efficacy</h5>
                                    <div className="rule-container">
                                        <p>Average Time Delay [%]: { this.state.activeItem.results.balanced.time }%</p>
                                        <p>Total: { this.state.activeItem.results.balanced.total } requests</p>
                                        <p>True Positive Rate: { this.state.activeItem.results.balanced.tpr }%</p>
                                        <p>False Positive Rate: { this.state.activeItem.results.balanced.fpr }%</p>
                                        <p>True Negative Rate: { this.state.activeItem.results.balanced.tnr }%</p>
                                        <p>False Negative Rate: { this.state.activeItem.results.balanced.fnr }%</p>
                                    </div>
                                    <div className="plot-container">
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
                                                x: this.state.activeItem.results.balanced.tpr, 
                                                y: this.state.activeItem.results.balanced.tnr
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
                                <div className="rule-container">
                                    <p>Average Time Delay [%]: { this.state.activeItem.results.conventional.time }%</p>
                                    <p>Total: { this.state.activeItem.results.conventional.total } requests</p>
                                    <p>True Positive Rate: { this.state.activeItem.results.conventional.tpr }%</p>
                                    <p>False Positive Rate: { this.state.activeItem.results.conventional.fpr }%</p>
                                    <p>True Negative Rate: { this.state.activeItem.results.conventional.tnr }%</p>
                                    <p>False Negative Rate: { this.state.activeItem.results.conventional.fnr }%</p>
                                </div>
                                <div className="plot-container">
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
                                            x: this.state.activeItem.results.conventional.tpr, 
                                            y: this.state.activeItem.results.conventional.tnr
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
                                <div className="rule-container">
                                    <p>Average Time Delay [%]: { this.state.activeItem.results.unconventional.time }%</p>
                                    <p>Total: { this.state.activeItem.results.unconventional.total } requests</p>
                                    <p>True Positive Rate: { this.state.activeItem.results.unconventional.tpr }%</p>
                                    <p>False Positive Rate: { this.state.activeItem.results.unconventional.fpr }%</p>
                                    <p>True Negative Rate: { this.state.activeItem.results.unconventional.tnr }%</p>
                                    <p>False Negative Rate: { this.state.activeItem.results.unconventional.fnr }%</p>
                                </div>
                                <div className="plot-container">
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
                                        <ReferenceLine  y={75} stroke="red" strokeDasharray="4 4" />
                                        <ReferenceLine x={75} stroke="red" strokeDasharray="4 4" />
                                        <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                                        <Scatter 
                                            name="Efficacy"
                                            data={[{
                                            x: this.state.activeItem.results.unconventional.tpr, 
                                            y: this.state.activeItem.results.unconventional.tnr
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
            </Modal>
        );
    }

}