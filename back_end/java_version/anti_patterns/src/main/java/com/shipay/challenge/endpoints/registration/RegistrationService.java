package com.shipay.challenge.endpoints.registration;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class RegistrationService {

    @Autowired
    private CustomerRepository repository;

    public void save(Customer customer) {
        repository.save(customer);
    }
    
    public Customer getCustomerById(Long id) {
        return repository.findById(id).orElse(null);
    }
}
