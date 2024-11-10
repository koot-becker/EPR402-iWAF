import React, { Component } from "react";
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

export default class CustomModal extends Component {
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

  handleSettingsChange = (e) => {
    let { name, value } = e.target;

    if (e.target.type === "checkbox") {
      value = e.target.checked;
    }

    const activeItem = { ...this.state.activeItem, settings: { ...this.state.activeItem.settings, [name]: value } };

    this.setState({ activeItem });
  }

  render() {
    const { toggle, onSave } = this.props;

    return (
      <Modal isOpen={true} toggle={toggle} size='lg'>
      <ModalHeader toggle={toggle}>WAF Configuration</ModalHeader>
      <ModalBody>
        <Form>
        <h5>WAF Information</h5>
        <FormGroup>
          <div className="row">
            <div className="col-sm-6">
              <Label for="waf-name">Name</Label>
              <Input
              type="text"
              id="waf-name"
              name="name"
              value={this.state.activeItem.name}
              onChange={this.handleChange}
              placeholder="Enter WAF Name"
              />
            </div>
            <div className="col-sm-6">
              <Label for="waf-description">Description</Label>
              <Input
              type="text"
              id="waf-description"
              name="description"
              value={this.state.activeItem.description}
              onChange={this.handleChange}
              placeholder="Enter WAF Description"
              />
            </div>
          </div>
        </FormGroup>
        <FormGroup>
          <div className="row">
            <div className="col-sm-6">
              <Label for="waf-address">WAF Address</Label>
              <Input
              type="text"
              id="waf-address"
              name="waf_address"
              value={this.state.activeItem.waf_address}
              onChange={this.handleChange}
              placeholder="Enter WAF Address"
              />
            </div>
            <div className="col-sm-6">
              <Label for="app-address">App Address</Label>
              <Input
              type="text"
              id="app-address"
              name="app_address"
              value={this.state.activeItem.app_address}
              onChange={this.handleChange}
              placeholder="Enter App Address"
              />
            </div>
          </div>
        </FormGroup>
        <FormGroup>
          <div className="row">
            <div className="col-sm-3">
              <Label for="total-requests">Total Requests</Label>
              <Input
              type="number"
              id="total-requests"
              name="total_requests"
              value={this.state.activeItem.total_requests}
              onChange={this.handleChange}
              placeholder="Enter Total Requests"
              />
            </div>
            <div className="col-sm-3">
              <Label for="allowed-requests">Allowed Requests</Label>
              <Input
              type="number"
              id="allowed-requests"
              name="allowed_requests"
              value={this.state.activeItem.allowed_requests}
              onChange={this.handleChange}
              placeholder="Enter Allowed Requests"
              />
            </div>
            <div className="col-sm-3">
              <Label for="blocked-requests">Blocked Requests</Label>
              <Input
              type="number"
              id="blocked-requests"
              name="blocked_requests"
              value={this.state.activeItem.blocked_requests}
              onChange={this.handleChange}
              placeholder="Enter Blocked Requests"
              />
            </div>
            <div className="col-sm-3">
              <Label for="average-time">Average Time</Label>
              <Input
              type="number"
              id="total-time"
              name="total_time"
              value={this.state.activeItem.total_time}
              onChange={this.handleChange}
              placeholder="Enter Total Time"
              />
            </div>
          </div>
        </FormGroup>
        </Form>
        <Form>
        <h5 style={{ marginTop: "20px" }}>WAF Settings</h5>
        <div className="row rule-container">
            <div className="col-sm-6">
              <FormGroup check>
                <Label check>
                <Input
                  type="checkbox"
                  name="app_enabled"
                  checked={this.state.activeItem.app_enabled}
                  onChange={this.handleChange}
                />
                App Enabled
                </Label>
              </FormGroup>
            </div>
            <div className="col-sm-6">
              <FormGroup check>
                <Label check>
                <Input
                  type="checkbox"
                  name="waf_enabled"
                  checked={this.state.activeItem.waf_enabled}
                  onChange={this.handleChange}
                />
                WAF Enabled
                </Label>
              </FormGroup>
            </div>
          </div>
        <h6 style={{ marginTop: "20px" }}>Rule Settings</h6>
        <div className="row rule-container">
            <div className="col-sm-3">
              <FormGroup check>
                <Label check>
                <Input
                  type="checkbox"
                  name="block_remote_addr"
                  checked={this.state.activeItem.settings.block_remote_addr}
                  onChange={this.handleSettingsChange}
                />
                Block Addresses
                </Label>
              </FormGroup>
            </div>
            <div className="col-sm-3">
              <FormGroup check>
                <Label check>
                <Input
                  type="checkbox"
                  name="block_user_agent"
                  checked={this.state.activeItem.settings.block_user_agent}
                  onChange={this.handleSettingsChange}
                />
                Block User Agent
                </Label>
              </FormGroup>
            </div>
            <div className="col-sm-3">
              <FormGroup check>
                <Label check>
                <Input
                  type="checkbox"
                  name="block_path"
                  checked={this.state.activeItem.settings.block_path}
                  onChange={this.handleSettingsChange}
                />
                Block Path
                </Label>
              </FormGroup>
            </div>
            <div className="col-sm-3">
              <FormGroup check>
                <Label check>
                <Input
                  type="checkbox"
                  name="block_query_string"
                  checked={this.state.activeItem.settings.block_query_string}
                  onChange={this.handleSettingsChange}
                />
                Block Query String
                </Label>
              </FormGroup>
            </div>
          </div>
          <div className="row">
            <div className="col-sm-4 rule-container">
              <h6 style={{ marginTop: "20px" }}>Token Blocking</h6>
              <FormGroup check>
                <Label check_token>
                <Input
                  type="checkbox"
                  name="check_token"
                  checked={this.state.activeItem.settings.check_token}
                  onChange={this.handleSettingsChange}
                />
                Enabled
                </Label>
              </FormGroup>
            </div>
            <div className="col-sm-4 rule-container">
              <h6 style={{ marginTop: "20px" }}>Signature Detection</h6>
              <FormGroup check>
                <Label check>
                <Input
                  type="checkbox"
                  name="check_signature"
                  checked={this.state.activeItem.settings.check_signature}
                  onChange={this.handleSettingsChange}
                />
                Enabled
                </Label>
              </FormGroup>
            </div>
            <div className="col-sm-4 rule-container">
              <h6 style={{ marginTop: "20px" }}>Anomaly Detection</h6>
              <FormGroup check>
                <Label check>
                <Input
                  type="checkbox"
                  name="check_anomaly"
                  checked={this.state.activeItem.settings.check_anomaly}
                  onChange={this.handleSettingsChange}
                />
                Enabled
                </Label>
              </FormGroup>
            </div>
          </div>
        </Form>
        <Form style={{ marginTop: "20px"}}>
        <h5>Rule Configuration</h5>
        <div className="row">
          <div className="col-sm-6 rule-container">
            <FormGroup>
              <div className="row" style={{ marginBottom: "10px" }}>
                <div className="col-md-8">
                  <Label for="blocked-ips" style={{ marginTop: "10px"}}>Blocked IP's</Label>
                </div>
                <div className="col-md-4">
                  <Button
                  color="primary"
                  onClick={() => {
                    const blocked_ips = [...this.state.activeItem.rules.blocked_ips, ""];
                    const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_ips } };
                    this.setState({ activeItem });
                  }}
                  style={{ width: "100%" }}
                  >
                    Add
                  </Button>
                </div>
              </div>
              {this.state.activeItem.rules.blocked_ips.map((ip, index) => (
              <div key={index} style={{ display: "flex", marginBottom: "10px" }} className="row">
                <div className="col-md-8">
                <Input
                type="text"
                id={`blocked-ip-${index}`}
                name={`blocked_ip_${index}`}
                value={ip}
                onChange={(e) => {
                  const blocked_ips = [...this.state.activeItem.rules.blocked_ips];
                  blocked_ips[index] = e.target.value;
                  const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_ips } };
                  this.setState({ activeItem });
                }}
                placeholder="Enter Blocked IP"
                />
                </div>
                <div className="col-md-4">
                <Button
                color="danger"
                onClick={() => {
                  const blocked_ips = this.state.activeItem.rules.blocked_ips.filter((_, i) => i !== index);
                  const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_ips } };
                  this.setState({ activeItem });
                }}
                style={{ width: "100%" }}
                >
                Remove
                </Button>
                </div>
              </div>
              ))}
            </FormGroup>
          </div>
          <div className="col-sm-6 rule-container">
            <FormGroup>
              <div className="row" style={{ marginBottom: "10px" }}>
                <div className="col-md-8">
                  <Label for="blocked-user-agents" style={{ marginTop: "10px"}}>Blocked User Agents</Label>
                </div>
                <div className="col-md-4">
                  <Button
                  color="primary"
                  onClick={() => {
                    const blocked_user_agents = [...this.state.activeItem.rules.blocked_user_agents, ""];
                    const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_user_agents } };
                    this.setState({ activeItem });
                  }}
                  style={{ width: "100%" }}
                  >
                  Add
                  </Button>
                </div>
              </div>
              {this.state.activeItem.rules.blocked_user_agents.map((user_agent, index) => (
              <div key={index} style={{ display: "flex", alignItems: "center", marginBottom: "10px" }} className="row">
                <div className="col-md-8">
                  <Input
                  type="text"
                  id={`blocked-user-agent-${index}`}
                  name={`blocked_user_agent_${index}`}
                  value={user_agent}
                  onChange={(e) => {
                    const blocked_user_agents = [...this.state.activeItem.rules.blocked_user_agents];
                    blocked_user_agents[index] = e.target.value;
                    const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_user_agents } };
                    this.setState({ activeItem });
                  }}
                  placeholder="Enter Blocked User Agent"
                  />
                </div>
                <div className="col-md-4">
                  <Button
                  color="danger"
                  onClick={() => {
                    const blocked_user_agents = this.state.activeItem.rules.blocked_user_agents.filter((_, i) => i !== index);
                    const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_user_agents } };
                    this.setState({ activeItem });
                  }}
                  style={{ width: "100%" }}
                  >
                  Remove
                  </Button>
                </div>
              </div>
              ))}
            </FormGroup>
          </div>
        </div>
        <div className="row">
          <div className="col-md-6 rule-container">
            <FormGroup>
              <div className="row" style={{ marginBottom: "10px" }}>
                <div className="col-md-8">
                  <Label for="blocked-paths" style={{ marginTop: "10px"}}>Blocked Paths</Label>
                </div>
                <div className="col-md-4">
                  <Button
                  color="primary"
                  onClick={() => {
                    const blocked_paths = [...this.state.activeItem.rules.blocked_paths, ""];
                    const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_paths } };
                    this.setState({ activeItem });
                  }}
                  style={{ width: "100%" }}
                  >
                  Add
                  </Button>
                </div>
              </div>
              {this.state.activeItem.rules.blocked_paths.map((path, index) => (
              <div key={index} style={{ display: "flex", marginBottom: "10px" }} className="row">
                <div className="col-md-8">
                  <Input
                  type="text"
                  id={`blocked-path-${index}`}
                  name={`blocked_path_${index}`}
                  value={path}
                  onChange={(e) => {
                    const blocked_paths = [...this.state.activeItem.rules.blocked_paths];
                    blocked_paths[index] = e.target.value;
                    const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_paths } };
                    this.setState({ activeItem });
                  }}
                  placeholder="Enter Blocked Path"
                  />
                </div>
                <div className="col-md-4">
                  <Button
                  color="danger"
                  onClick={() => {
                    const blocked_paths = this.state.activeItem.rules.blocked_paths.filter((_, i) => i !== index);
                    const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_paths } };
                    this.setState({ activeItem });
                  }}
                  style={{ width: "100%" }}
                  >
                  Remove
                  </Button>
                </div>
              </div>
              ))}
            </FormGroup>
          </div>
          <div className="col-md-6 rule-container">
            <FormGroup>
              <div className="row" style={{ marginBottom: "10px" }}>
                <div className="col-md-8">
                  <Label for="blocked-query-strings" style={{ marginTop: "10px"}}>Blocked Query Strings</Label>
                </div>
                <div className="col-md-4">
                  <Button
                  color="primary"
                  onClick={() => {
                    const blocked_query_strings = [...this.state.activeItem.rules.blocked_query_strings, ""];
                    const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_query_strings } };
                    this.setState({ activeItem });
                  }}
                  style={{ width: "100%" }}
                  >
                  Add
                  </Button>
                </div>
              </div>
              {this.state.activeItem.rules.blocked_query_strings.map((query_string, index) => (
              <div key={index} style={{ display: "flex", alignItems: "center", marginBottom: "10px" }} className="row">
                <div className="col-md-8">
                <Input
                type="text"
                id={`blocked-query-string-${index}`}
                name={`blocked_query_string_${index}`}
                value={query_string}
                onChange={(e) => {
                  const blocked_query_strings = [...this.state.activeItem.rules.blocked_query_strings];
                  blocked_query_strings[index] = e.target.value;
                  const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_query_strings } };
                  this.setState({ activeItem });
                }}
                placeholder="Enter Blocked Query String"
                />
                </div>
                <div className="col-md-4">
                <Button
                color="danger"
                onClick={() => {
                  const blocked_query_strings = this.state.activeItem.rules.blocked_query_strings.filter((_, i) => i !== index);
                  const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_query_strings } };
                  this.setState({ activeItem });
                }}
                style={{ width: "100%" }}
                >
                Remove
                </Button>
                </div>
              </div>
              ))}
            </FormGroup>
          </div>
        </div>
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