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
        <ModalHeader toggle={toggle}>WAF Item</ModalHeader>
        <ModalBody>
          <Form>
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
              <Label for="waf-details-path">WAF Details Path</Label>
              <Input
                type="text"
                id="waf-details-path"
                name="waf_details_path"
                value={this.state.activeItem.waf_details_path}
                onChange={this.handleChange}
                placeholder="Enter WAF Details Path"
              />
            </FormGroup>
            <FormGroup>
              <Label for="start-waf-path">Start WAF Path</Label>
              <Input
                type="text"
                id="start-waf-path"
                name="start_waf_path"
                value={this.state.activeItem.start_waf_path}
                onChange={this.handleChange}
                placeholder="Enter Start WAF Path"
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
              <Label for="start-web-app-path">Start Web App Path</Label>
              <Input
                type="text"
                id="start-web-app-path"
                name="start_web_app_path"
                value={this.state.activeItem.start_web_app_path}
                onChange={this.handleChange}
                placeholder="Enter Start Web App Path"
              />
            </FormGroup>
            <FormGroup>
              <Label for="web-app-address">Web App Address</Label>
              <Input
                type="text"
                id="web-app-address"
                name="web_app_address"
                value={this.state.activeItem.web_app_address}
                onChange={this.handleChange}
                placeholder="Enter Web App Address"
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
            <FormGroup>
              <Label for="threats-detected">Threats Detected</Label>
              <Input
                type="number"
                id="threats-detected"
                name="threats_detected"
                value={this.state.activeItem.threats_detected}
                onChange={this.handleChange}
                placeholder="Enter Threats Detected"
              />
            </FormGroup>
            <FormGroup check>
              <Label check>
                <Input
                  type="checkbox"
                  name="enabled"
                  checked={this.state.activeItem.enabled}
                  onChange={this.handleChange}
                />
                Enabled
              </Label>
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