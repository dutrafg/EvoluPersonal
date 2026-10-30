#!/usr/bin/env node
'use strict';
/* Testes estruturais da reformulação premium. Rodar: node tests-design.cjs */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname,'dist','index.html'),'utf8');
const check = (needle,label) => assert(html.includes(needle),label);
check('class="hero hero-dashboard"','Dashboard premium ausente');
check('class="rail-name"','Identidade da barra lateral ausente');
check('EVOLU<span>PERSONAL</span>','Marca atualizada ausente');
check("['home','Dashboard']", 'Navegação da Dashboard ausente');
check('Biblioteca de movimentos · GIFs associados aos exercícios oficiais','Descrição da biblioteca incorreta');
check('.md-gallery .md-gallery-grid{display:grid;grid-template-columns:repeat(5','Grade original não preservada');
check('.md-gallery .md-exercise:hover','Interação dos cards ausente');
check('@media(max-width:640px)', 'Layout móvel ausente');
check('@media(max-width:365px)', 'Layout para telas estreitas ausente');
check('prefers-reduced-motion:reduce', 'Preferência de movimento reduzido não atendida');
check("const VERSION=2,KEY='evolupersonal.alpha1'","Persistência de dados alterada");
check("const all=mdLibraryMatches()",'Filtros da biblioteca alterados');
check("const count=catalog.filter(e=>!!mdMediaSource(e)).length",'Contagem de GIFs não preservada');
for(const func of ['studentModal','workoutModal','sessionView','exportData','importData','toggleTheme'])check('function '+func+'(',func+' removida');
assert.equal((html.match(/<script>/g)||[]).length,1,'Script principal inesperadamente dividido');
console.log('PASS: estrutura, responsividade, biblioteca MD500, funções e persistência da reformulação visual.');
