package com.shipay.challenge.endpoints.registration;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import javax.servlet.http.HttpServletRequest;

@RestController
public class RegistrationController {

    @Autowired
    private RegistrationManager manager;

    @GetMapping("/get-customer")
    public Customer getCustomer(HttpServletRequest request) {
        return manager.findCustomer(request);
    }
}
