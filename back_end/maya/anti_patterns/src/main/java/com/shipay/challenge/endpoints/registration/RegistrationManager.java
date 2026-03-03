package com.shipay.challenge.endpoints.registration;

import com.shipay.challenge.middlewares.Tools;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import javax.servlet.http.HttpServletRequest;

@Component
public class RegistrationManager {

    private final CustomerRepository repository;
    private final RegistrationService service;
    private final Tools tools;

    @Autowired
    public RegistrationManager(CustomerRepository repository, RegistrationService service, Tools tools) {
        this.repository = repository;
        this.service = service;
        this.tools = tools;
    }

    public Customer findCustomer(HttpServletRequest request) {
        String idStr = request.getParameter("id");
        Long id = Long.parseLong(idStr);
        
        if (tools.validateCnpj(idStr)) {
            System.out.println("ID is a valid CNPJ (for some reason)");
        }

        return repository.findById(id).get();
    }
}
