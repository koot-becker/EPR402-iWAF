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

  render() {
    const { toggle, onSave } = this.props;

    return (
      <Modal isOpen={true} toggle={toggle}>
      <ModalHeader toggle={toggle}>WAF Configuration</ModalHeader>
      <ModalBody>
        <Form>
        <h5>WAF Information</h5>
        <FormGroup>
          <Label for="waf-name">Name</Label>
          <Input
          type="text"
          id="waf-name"
          name="name"
          value={this.state.activeItem.name}
          onChange={this.handleChange}
          placeholder="Enter WAF Name"
          />
        </FormGroup>
        <FormGroup>
          <Label for="waf-description">Description</Label>
          <Input
          type="text"
          id="waf-description"
          name="description"
          value={this.state.activeItem.description}
          onChange={this.handleChange}
          placeholder="Enter WAF Description"
          />
        </FormGroup>
        <FormGroup>
          <Label for="waf-address">WAF Address</Label>
          <Input
          type="text"
          id="waf-address"
          name="waf_address"
          value={this.state.activeItem.waf_address}
          onChange={this.handleChange}
          placeholder="Enter WAF Address"
          />
        </FormGroup>
        <FormGroup>
          <Label for="app-address">App Address</Label>
          <Input
          type="text"
          id="app-address"
          name="app_address"
          value={this.state.activeItem.app_address}
          onChange={this.handleChange}
          placeholder="Enter App Address"
          />
        </FormGroup>
        <FormGroup>
          <Label for="total-requests">Total Requests</Label>
          <Input
          type="number"
          id="total-requests"
          name="total_requests"
          value={this.state.activeItem.total_requests}
          onChange={this.handleChange}
          placeholder="Enter Total Requests"
          />
        </FormGroup>
        <FormGroup>
          <Label for="allowed-requests">Allowed Requests</Label>
          <Input
          type="number"
          id="allowed-requests"
          name="allowed_requests"
          value={this.state.activeItem.allowed_requests}
          onChange={this.handleChange}
          placeholder="Enter Allowed Requests"
          />
        </FormGroup>
        <FormGroup>
          <Label for="blocked-requests">Blocked Requests</Label>
          <Input
          type="number"
          id="blocked-requests"
          name="blocked_requests"
          value={this.state.activeItem.blocked_requests}
          onChange={this.handleChange}
          placeholder="Enter Blocked Requests"
          />
        </FormGroup>
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
        </Form>
        <Form>
        <h5 style={{ marginTop: "20px" }}>WAF Settings</h5>
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
        <h6 style={{ marginTop: "20px" }}>Rule Configuration</h6>
        <FormGroup check>
          <Label check>
          <Input
            type="checkbox"
            name="block_remote_addr"
            checked={this.state.activeItem.settings.rule_settings.block_remote_addr}
            onChange={this.handleChange}
          />
          Block Remote Addresses
          </Label>
        </FormGroup>
        <FormGroup check>
          <Label check>
          <Input
            type="checkbox"
            name="block_user_agent"
            checked={this.state.activeItem.settings.rule_settings.block_user_agent}
            onChange={this.handleChange}
          />
          Block User Agent
          </Label>
        </FormGroup>
        <FormGroup check>
          <Label check>
          <Input
            type="checkbox"
            name="block_path"
            checked={this.state.activeItem.settings.rule_settings.block_path}
            onChange={this.handleChange}
          />
          Block Path
          </Label>
        </FormGroup>
        <FormGroup check>
          <Label check>
          <Input
            type="checkbox"
            name="block_query_string"
            checked={this.state.activeItem.settings.rule_settings.block_query_string}
            onChange={this.handleChange}
          />
          Block Query String
          </Label>
        </FormGroup>
        <h6 style={{ marginTop: "20px" }}>Token Configuration</h6>
        <FormGroup check>
          <Label check>
          <Input
            type="checkbox"
            name="check_token"
            checked={this.state.activeItem.settings.token_settings.check_token}
            onChange={this.handleChange}
          />
          Block Invalid JWT Token
          </Label>
        </FormGroup>

        <h6 style={{ marginTop: "20px" }}>Signature Detection Configuration</h6>
        <FormGroup check>
          <Label check>
          <Input
            type="checkbox"
            name="check_signature"
            checked={this.state.activeItem.settings.signature_settings.check_signature}
            onChange={this.handleChange}
          />
          Enable Signature Detection
          </Label>
        </FormGroup>
        <h6 style={{ marginTop: "20px" }}>Anomaly Detection Configuration</h6>
        <FormGroup check>
          <Label check>
          <Input
            type="checkbox"
            name="check_anomaly"
            checked={this.state.activeItem.settings.anomaly_settings.check_anomaly}
            onChange={this.handleChange}
          />
          Enable Anomaly Detection
          </Label>
        </FormGroup>
        </Form>
        <Form>
        <h5 style={{ justifyContent: "20px" }}>Rule Configuration</h5>
        <FormGroup>
          <div className="row">
            <div className="col-md-10">
              <Label for="blocked-ips" style={{ marginTop: "10px"}}>Blocked IP's</Label>
            </div>
            <div className="col-md-2">
              <Button
              color="primary"
              onClick={() => {
                const blocked_ips = [...this.state.activeItem.rules.blocked_ips, ""];
                const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_ips } };
                this.setState({ activeItem });
              }}
              >
                Add
              </Button>
            </div>
          </div>
          {this.state.activeItem.rules.blocked_ips.map((ip, index) => (
          <div key={index} style={{ display: "flex", alignItems: "center", marginBottom: "10px" }}>
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
            <Button
            color="danger"
            onClick={() => {
              const blocked_ips = this.state.activeItem.rules.blocked_ips.filter((_, i) => i !== index);
              const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_ips } };
              this.setState({ activeItem });
            }}
            style={{ marginLeft: "10px" }}
            >
            Remove
            </Button>
          </div>
          ))}
        </FormGroup>
        <FormGroup>
          <div className="row">
            <div className="col-md-10">
              <Label for="blocked-user-agents" style={{ marginTop: "10px"}}>Blocked User Agents</Label>
            </div>
            <div className="col-md-2">
              <Button
              color="primary"
              onClick={() => {
                const blocked_user_agents = [...this.state.activeItem.rules.blocked_user_agents, ""];
                const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_user_agents } };
                this.setState({ activeItem });
              }}
              >
              Add
              </Button>
            </div>
          </div>
          {this.state.activeItem.rules.blocked_user_agents.map((user_agent, index) => (
          <div key={index} style={{ display: "flex", alignItems: "center", marginBottom: "10px" }}>
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
            <Button
            color="danger"
            onClick={() => {
              const blocked_user_agents = this.state.activeItem.rules.blocked_user_agents.filter((_, i) => i !== index);
              const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_user_agents } };
              this.setState({ activeItem });
            }}
            style={{ marginLeft: "10px" }}
            >
            Remove
            </Button>
          </div>
          ))}
        </FormGroup>
        <FormGroup>
          <div className="row">
            <div className="col-md-10">
              <Label for="blocked-paths" style={{ marginTop: "10px"}}>Blocked Paths</Label>
            </div>
            <div className="col-md-2">
              <Button
              color="primary"
              onClick={() => {
                const blocked_paths = [...this.state.activeItem.rules.blocked_paths, ""];
                const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_paths } };
                this.setState({ activeItem });
              }}
              >
              Add
              </Button>
            </div>
          </div>
          {this.state.activeItem.rules.blocked_paths.map((path, index) => (
          <div key={index} style={{ display: "flex", alignItems: "center", marginBottom: "10px" }}>
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
            <Button
            color="danger"
            onClick={() => {
              const blocked_paths = this.state.activeItem.rules.blocked_paths.filter((_, i) => i !== index);
              const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_paths } };
              this.setState({ activeItem });
            }}
            style={{ marginLeft: "10px" }}
            >
            Remove
            </Button>
          </div>
          ))}
        </FormGroup>
        <FormGroup>
          <div className="row">
            <div className="col-md-10">
              <Label for="blocked-query-strings" style={{ marginTop: "10px"}}>Blocked Query Strings</Label>
            </div>
            <div className="col-md-2">
              <Button
              color="primary"
              onClick={() => {
                const blocked_query_strings = [...this.state.activeItem.rules.blocked_query_strings, ""];
                const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_query_strings } };
                this.setState({ activeItem });
              }}
              >
              Add
              </Button>
            </div>
          </div>
          {this.state.activeItem.rules.blocked_query_strings.map((query_string, index) => (
          <div key={index} style={{ display: "flex", alignItems: "center", marginBottom: "10px" }}>
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
            <Button
            color="danger"
            onClick={() => {
              const blocked_query_strings = this.state.activeItem.rules.blocked_query_strings.filter((_, i) => i !== index);
              const activeItem = { ...this.state.activeItem, rules: { ...this.state.activeItem.rules, blocked_query_strings } };
              this.setState({ activeItem });
            }}
            style={{ marginLeft: "10px" }}
            >
            Remove
            </Button>
          </div>
          ))}
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